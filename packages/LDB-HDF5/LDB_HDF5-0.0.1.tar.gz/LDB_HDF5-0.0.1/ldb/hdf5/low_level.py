from __future__ import absolute_import

from ldb.hdf5._hdf5 import lib as hdf5_lib, ffi as hdf5_ffi
from ldb.hdf5.exceptions import DatasetExistsError, AttributeExistsError
from ldb.hdf5.context import CountingContextManager

"""
The purpose of this module is to provide pythonic wrappers for the HDF5 C API.
These classes provided things like context managers to handle closing of
resources. They do not try to do things like convert python types to HDF5
types or provide better interfaces for accessing data (like slices). For any of
that see the high_level module.
"""

# TODO: Use counting context manager AND test (double context enter, and make
# sure final context exit function being called
# TODO: Make datasets grab context for files/groups used to open/create them,
# attributes for datasets/groups, etc, etc
# TODO: Handle herr_t returns
# TODO: Make sure to add error text from HDF5 to exceptions
# TODO: Allow CData for any array and test
# TODO: If input is bytes instead of str, don't encode

class HDF5File_(CountingContextManager):
    def __init__(self, file_id):
        super(HDF5File_, self).__init__()
        self.file_id = file_id

    @property
    def loc_id(self):
        return self.file_id

    @classmethod
    def create(cls, filename, truncate_if_exists=False):
        filename = filename.encode("utf8")

        flags = (hdf5_lib.H5F_ACC_TRUNC if truncate_if_exists else
                 hdf5_lib.H5F_ACC_EXCL)
        # TODO: Figure out what the creation/access properties are
        file_id = hdf5_lib.H5Fcreate(filename, flags, hdf5_lib.H5P_DEFAULT,
                                     hdf5_lib.H5P_DEFAULT)
        if file_id < 0:
            raise IOError # TODO: py3.3 FileExistsError

        return cls(file_id)

    @classmethod
    def open(cls, filename, read_only=False):
        filename = filename.encode("utf8")

        flags = (hdf5_lib.H5F_ACC_RDONLY if read_only else
                 hdf5_lib.H5F_ACC_RDWR)
        # TODO: Figure out what the access properties are
        file_id = hdf5_lib.H5Fopen(filename, flags, hdf5_lib.H5P_DEFAULT)
        if file_id < 0:
            raise IOError # TODO: py3.3 FileExistsError

        return cls(file_id)

    def flush(self, scope):
        return hdf5_lib.H5Fflush(self.file_id, scope)

    def _final_context_exit(self, exc_type, exc_value, traceback):
        hdf5_lib.H5Fclose(self.file_id)
        self.file_id = None


class HDF5Dataspace_(CountingContextManager):
    def __init__(self, dataspace_id):
        super(HDF5Dataspace_, self).__init__()
        self.dataspace_id = dataspace_id

    @classmethod
    def create(cls, type_):
        return cls(hdf5_lib.H5Screate(type_))

    @classmethod
    def create_simple(cls, current_dims, maximum_dims=None):
        if maximum_dims is None:
            maximum_dims = hdf5_ffi.NULL
        elif not isinstance(maximum_dims, hdf5_ffi.CData):
            maximum_dims = hdf5_ffi.new('hsize_t[]', maximum_dims)

        if not isinstance(current_dims, hdf5_ffi.CData):
            current_dims = hdf5_ffi.new('hsize_t[]', current_dims)

        dataspace_id = hdf5_lib.H5Screate_simple(len(current_dims),
                                                 current_dims, maximum_dims)

        return cls(dataspace_id)

    def get_simple_extent_dims(self, dims, maximum_dims=None):
        if dims is None:
            dims = hdf5_ffi.NULL
        if maximum_dims is None:
            maximum_dims = hdf5_ffi.NULL

        return hdf5_lib.H5Sget_simple_extent_dims(self.dataspace_id, dims,
                                                  maximum_dims)

    def get_simple_extent_ndims(self):
        return hdf5_lib.H5Sget_simple_extent_ndims(self.dataspace_id)

    def select_hyperslab(self, select_operator, start, stride, count,
                         block=None):
        start = hdf5_ffi.new('hsize_t[]', start)
        if stride is None:
            stride = hdf5_ffi.NULL
        else:
            stride = hdf5_ffi.new('hsize_t[]', stride)
        count = hdf5_ffi.new('hsize_t[]', count)
        if block is None:
            block = hdf5_ffi.NULL
        else:
            block = hdf5_ffi.new('hsize_t[]', block)
        hdf5_lib.H5Sselect_hyperslab(self.dataspace_id, select_operator, start,
                                     stride, count, block)

    def _final_context_exit(self, exc_type, exc_value, traceback):
        hdf5_lib.H5Sclose(self.dataspace_id)
        self.dataspace_id = None


class HDF5Dataset_(CountingContextManager):
    def __init__(self, dataset_id):
        super(HDF5Dataset_, self).__init__()
        self.dataset_id = dataset_id

    @property
    def loc_id(self):
        return self.dataset_id

    @classmethod
    def create2(cls, hdf5_loc, dataset_name, datatype, dataspace,
               link_creation_properties=None, dataset_creation_properties=None,
               dataset_access_properties=None):
        dataset_name = dataset_name.encode("utf8")

        if link_creation_properties is None:
            link_creation_properties = hdf5_lib.H5P_DEFAULT
        if dataset_creation_properties is None:
            dataset_creation_properties = hdf5_lib.H5P_DEFAULT
        if dataset_access_properties is None:
            dataset_access_properties = hdf5_lib.H5P_DEFAULT

        dataset_id = hdf5_lib.H5Dcreate2(hdf5_loc.loc_id, dataset_name,
                                         datatype.type_id,
                                         dataspace.dataspace_id,
                                         link_creation_properties,
                                         dataset_creation_properties,
                                         dataset_access_properties)

        if dataset_id < 0:
            raise DatasetExistsError

        return cls(dataset_id)

    @classmethod
    def open2(cls, hdf5_loc, dataset_name, dataset_access_properties=None):
        dataset_name = dataset_name.encode("utf8")

        if dataset_access_properties is None:
            dataset_access_properties = hdf5_lib.H5P_DEFAULT

        dataset_id = hdf5_lib.H5Dopen2(hdf5_loc.loc_id, dataset_name,
                                       dataset_access_properties)

        return cls(dataset_id)

    def write(self, mem_type, data, mem_space=None, file_space=None,
              transfer_properties=None):
        if mem_space is None:
            mem_space = hdf5_lib.H5S_ALL
        else:
            mem_space = mem_space.dataspace_id
        if file_space is None:
            file_space = hdf5_lib.H5S_ALL
        else:
            file_space = file_space.dataspace_id
        # TODO: Handle non-None properties
        if transfer_properties is None:
            transfer_properties = hdf5_lib.H5P_DEFAULT

        hdf5_lib.H5Dwrite(self.dataset_id, mem_type.type_id, mem_space,
                          file_space, transfer_properties, data)

    def read(self, mem_type, data, mem_space=None, file_space=None,
             transfer_properties=None):
        if mem_space is None:
            mem_space = hdf5_lib.H5S_ALL
        else:
            mem_space = mem_space.dataspace_id
        if file_space is None:
            file_space = hdf5_lib.H5S_ALL
        else:
            file_space = file_space.dataspace_id
        # TODO: Handle non-None properties
        if transfer_properties is None:
            transfer_properties = hdf5_lib.H5P_DEFAULT

        hdf5_lib.H5Dread(self.dataset_id, mem_type.type_id, mem_space,
                         file_space, transfer_properties, data)

    def get_space(self):
        return HDF5Dataspace_(hdf5_lib.H5Dget_space(self.dataset_id))

    def get_type(self):
        return HDF5Type_(hdf5_lib.H5Dget_type(self.dataset_id))

    def _final_context_exit(self, exc_type, exc_value, traceback):
        hdf5_lib.H5Dclose(self.dataset_id)
        self.dataset_id = None


class HDF5Attribute_(CountingContextManager):
    def __init__(self, attribute_id):
        super(HDF5Attribute_, self).__init__()
        self.attribute_id = attribute_id

    @classmethod
    def create2(cls, hdf5_loc, attribute_name, datatype, dataspace,
                attribute_creation_properties=None,
                attribute_access_properties=None):
        attribute_name = attribute_name.encode("utf8")

        if attribute_creation_properties is None:
            attribute_creation_properties = hdf5_lib.H5P_DEFAULT
        if attribute_access_properties is None:
            attribute_access_properties = hdf5_lib.H5P_DEFAULT

        attribute_id = hdf5_lib.H5Acreate2(hdf5_loc.loc_id, attribute_name,
                                           datatype.type_id,
                                           dataspace.dataspace_id,
                                           attribute_creation_properties,
                                           attribute_access_properties)

        if attribute_id < 0:
            raise AttributeExistsError

        return cls(attribute_id)

    @classmethod
    def open(cls, hdf5_loc, attribute_name,
                attribute_access_properties=None):
        attribute_name = attribute_name.encode("utf8")

        if attribute_access_properties is None:
            attribute_access_properties = hdf5_lib.H5P_DEFAULT

        attribute_id = hdf5_lib.H5Aopen(hdf5_loc.loc_id, attribute_name,
                                        attribute_access_properties)

        return cls(attribute_id)

    def write(self, mem_type, data):
        hdf5_lib.H5Awrite(self.attribute_id, mem_type.type_id, data)

    def read(self, mem_type, data):
        hdf5_lib.H5Aread(self.attribute_id, mem_type.type_id, data)

    def get_space(self):
        return HDF5Dataspace_(hdf5_lib.H5Aget_space(self.attribute_id))

    def get_type(self):
        return HDF5Type_(hdf5_lib.H5Aget_type(self.attribute_id))

    def _final_context_exit(self, exc_type, exc_value, traceback):
        hdf5_lib.H5Aclose(self.attribute_id)
        self.attribute_id = None


class HDF5Type_(CountingContextManager):
    def __init__(self, type_id, no_close=False):
        super(HDF5Type_, self).__init__()
        self.type_id = type_id
        self.no_close = no_close

    @classmethod
    def create(cls, class_, size):
        return cls(hdf5_lib.H5Tcreate(class_, size))

    def copy(self):
        return HDF5Type_(hdf5_lib.H5Tcopy(self.type_id))

    def get_class(self):
        return hdf5_lib.H5Tget_class(self.type_id)

    def get_size(self):
        return hdf5_lib.H5Tget_size(self.type_id)

    def get_member_class(self, member_no):
        return hdf5_lib.H5Tget_member_class(self.type_id, member_no)

    def get_member_index(self, field_name):
        field_name = field_name.encode("utf8")

        field_name_cstr = hdf5_ffi.new('char[]', field_name)
        return hdf5_lib.H5Tget_member_index(self.type_id, field_name_cstr)

    def get_member_name(self, field_idx):
        bytes_ = hdf5_ffi.string(hdf5_lib.H5Tget_member_name(self.type_id,
                                                             field_idx))
        return bytes_.decode("utf8")

    def get_member_offset(self, memb_no):
        return hdf5_lib.H5Tget_member_offset(self.type_id, memb_no)

    def get_member_type(self, field_idx):
        type_id = hdf5_lib.H5Tget_member_type(self.type_id, field_idx)
        return HDF5Type_(type_id)

    def get_nmembers(self):
        return hdf5_lib.H5Tget_nmembers(self.type_id)

    def insert(self, name, offset, field_id):
        name = name.encode("utf8")
        return hdf5_lib.H5Tinsert(self.type_id, name, offset, field_id.type_id)

    def set_size(self, size):
        return hdf5_lib.H5Tset_size(self.type_id, size)

    def _initial_context_enter(self):
        if self.no_close:
            raise Exception("Can't use context manager on this hdf type.")

    def _final_context_exit(self, exc_type, exc_value, traceback):
        hdf5_lib.H5Tclose(self.type_id)
        self.type_id = None

class HDF5TypeBuiltin_(object):
    IEEE_F32BE = HDF5Type_(hdf5_lib.H5T_IEEE_F32BE, True)
    IEEE_F32LE = HDF5Type_(hdf5_lib.H5T_IEEE_F32LE, True)
    IEEE_F64BE = HDF5Type_(hdf5_lib.H5T_IEEE_F64BE, True)
    IEEE_F64LE = HDF5Type_(hdf5_lib.H5T_IEEE_F64LE, True)

    STD_I8BE = HDF5Type_(hdf5_lib.H5T_STD_I8BE, True)
    STD_I8LE = HDF5Type_(hdf5_lib.H5T_STD_I8LE, True)
    STD_I16BE = HDF5Type_(hdf5_lib.H5T_STD_I16BE, True)
    STD_I16LE = HDF5Type_(hdf5_lib.H5T_STD_I16LE, True)
    STD_I32BE = HDF5Type_(hdf5_lib.H5T_STD_I32BE, True)
    STD_I32LE = HDF5Type_(hdf5_lib.H5T_STD_I32LE, True)
    STD_I64BE = HDF5Type_(hdf5_lib.H5T_STD_I64BE, True)
    STD_I64LE = HDF5Type_(hdf5_lib.H5T_STD_I64LE, True)
    STD_U8BE = HDF5Type_(hdf5_lib.H5T_STD_U8BE, True)
    STD_U8LE = HDF5Type_(hdf5_lib.H5T_STD_U8LE, True)
    STD_U16BE = HDF5Type_(hdf5_lib.H5T_STD_U16BE, True)
    STD_U16LE = HDF5Type_(hdf5_lib.H5T_STD_U16LE, True)
    STD_U32BE = HDF5Type_(hdf5_lib.H5T_STD_U32BE, True)
    STD_U32LE = HDF5Type_(hdf5_lib.H5T_STD_U32LE, True)
    STD_U64BE = HDF5Type_(hdf5_lib.H5T_STD_U64BE, True)
    STD_U64LE = HDF5Type_(hdf5_lib.H5T_STD_U64LE, True)
    STD_B8BE = HDF5Type_(hdf5_lib.H5T_STD_B8BE, True)
    STD_B8LE = HDF5Type_(hdf5_lib.H5T_STD_B8LE, True)
    STD_B16BE = HDF5Type_(hdf5_lib.H5T_STD_B16BE, True)
    STD_B16LE = HDF5Type_(hdf5_lib.H5T_STD_B16LE, True)
    STD_B32BE = HDF5Type_(hdf5_lib.H5T_STD_B32BE, True)
    STD_B32LE = HDF5Type_(hdf5_lib.H5T_STD_B32LE, True)
    STD_B64BE = HDF5Type_(hdf5_lib.H5T_STD_B64BE, True)
    STD_B64LE = HDF5Type_(hdf5_lib.H5T_STD_B64LE, True)

    STD_REF_OBJ = HDF5Type_(hdf5_lib.H5T_STD_REF_OBJ, True)
    STD_REF_DSETREG = HDF5Type_(hdf5_lib.H5T_STD_REF_DSETREG, True)

    UNIX_D32BE = HDF5Type_(hdf5_lib.H5T_UNIX_D32BE, True)
    UNIX_D32LE = HDF5Type_(hdf5_lib.H5T_UNIX_D32LE, True)
    UNIX_D64BE = HDF5Type_(hdf5_lib.H5T_UNIX_D64BE, True)
    UNIX_D64LE = HDF5Type_(hdf5_lib.H5T_UNIX_D64LE, True)

    C_S1 = HDF5Type_(hdf5_lib.H5T_C_S1, True)
    FORTRAN_S1 = HDF5Type_(hdf5_lib.H5T_FORTRAN_S1, True)

    INTEL_I8 = HDF5Type_(hdf5_lib.H5T_INTEL_I8, True)
    INTEL_I16 = HDF5Type_(hdf5_lib.H5T_INTEL_I16, True)
    INTEL_I32 = HDF5Type_(hdf5_lib.H5T_INTEL_I32, True)
    INTEL_I64 = HDF5Type_(hdf5_lib.H5T_INTEL_I64, True)
    INTEL_U8 = HDF5Type_(hdf5_lib.H5T_INTEL_U8, True)
    INTEL_U16 = HDF5Type_(hdf5_lib.H5T_INTEL_U16, True)
    INTEL_U32 = HDF5Type_(hdf5_lib.H5T_INTEL_U32, True)
    INTEL_U64 = HDF5Type_(hdf5_lib.H5T_INTEL_U64, True)
    INTEL_B8 = HDF5Type_(hdf5_lib.H5T_INTEL_B8, True)
    INTEL_B16 = HDF5Type_(hdf5_lib.H5T_INTEL_B16, True)
    INTEL_B32 = HDF5Type_(hdf5_lib.H5T_INTEL_B32, True)
    INTEL_B64 = HDF5Type_(hdf5_lib.H5T_INTEL_B64, True)
    INTEL_F32 = HDF5Type_(hdf5_lib.H5T_INTEL_F32, True)
    INTEL_F64 = HDF5Type_(hdf5_lib.H5T_INTEL_F64, True)

    ALPHA_I8 = HDF5Type_(hdf5_lib.H5T_ALPHA_I8, True)
    ALPHA_I16 = HDF5Type_(hdf5_lib.H5T_ALPHA_I16, True)
    ALPHA_I32 = HDF5Type_(hdf5_lib.H5T_ALPHA_I32, True)
    ALPHA_I64 = HDF5Type_(hdf5_lib.H5T_ALPHA_I64, True)
    ALPHA_U8 = HDF5Type_(hdf5_lib.H5T_ALPHA_U8, True)
    ALPHA_U16 = HDF5Type_(hdf5_lib.H5T_ALPHA_U16, True)
    ALPHA_U32 = HDF5Type_(hdf5_lib.H5T_ALPHA_U32, True)
    ALPHA_U64 = HDF5Type_(hdf5_lib.H5T_ALPHA_U64, True)
    ALPHA_B8 = HDF5Type_(hdf5_lib.H5T_ALPHA_B8, True)
    ALPHA_B16 = HDF5Type_(hdf5_lib.H5T_ALPHA_B16, True)
    ALPHA_B32 = HDF5Type_(hdf5_lib.H5T_ALPHA_B32, True)
    ALPHA_B64 = HDF5Type_(hdf5_lib.H5T_ALPHA_B64, True)
    ALPHA_F32 = HDF5Type_(hdf5_lib.H5T_ALPHA_F32, True)
    ALPHA_F64 = HDF5Type_(hdf5_lib.H5T_ALPHA_F64, True)

    MIPS_I8 = HDF5Type_(hdf5_lib.H5T_MIPS_I8, True)
    MIPS_I16 = HDF5Type_(hdf5_lib.H5T_MIPS_I16, True)
    MIPS_I32 = HDF5Type_(hdf5_lib.H5T_MIPS_I32, True)
    MIPS_I64 = HDF5Type_(hdf5_lib.H5T_MIPS_I64, True)
    MIPS_U8 = HDF5Type_(hdf5_lib.H5T_MIPS_U8, True)
    MIPS_U16 = HDF5Type_(hdf5_lib.H5T_MIPS_U16, True)
    MIPS_U32 = HDF5Type_(hdf5_lib.H5T_MIPS_U32, True)
    MIPS_U64 = HDF5Type_(hdf5_lib.H5T_MIPS_U64, True)
    MIPS_B8 = HDF5Type_(hdf5_lib.H5T_MIPS_B8, True)
    MIPS_B16 = HDF5Type_(hdf5_lib.H5T_MIPS_B16, True)
    MIPS_B32 = HDF5Type_(hdf5_lib.H5T_MIPS_B32, True)
    MIPS_B64 = HDF5Type_(hdf5_lib.H5T_MIPS_B64, True)
    MIPS_F32 = HDF5Type_(hdf5_lib.H5T_MIPS_F32, True)
    MIPS_F64 = HDF5Type_(hdf5_lib.H5T_MIPS_F64, True)

    VAX_F32 = HDF5Type_(hdf5_lib.H5T_VAX_F32, True)
    VAX_F64 = HDF5Type_(hdf5_lib.H5T_VAX_F64, True)

    NATIVE_CHAR = HDF5Type_(hdf5_lib.H5T_NATIVE_CHAR, True)
    NATIVE_SCHAR = HDF5Type_(hdf5_lib.H5T_NATIVE_SCHAR, True)
    NATIVE_UCHAR = HDF5Type_(hdf5_lib.H5T_NATIVE_UCHAR, True)
    NATIVE_SHORT = HDF5Type_(hdf5_lib.H5T_NATIVE_SHORT, True)
    NATIVE_USHORT = HDF5Type_(hdf5_lib.H5T_NATIVE_USHORT, True)
    NATIVE_INT = HDF5Type_(hdf5_lib.H5T_NATIVE_INT, True)
    NATIVE_UINT = HDF5Type_(hdf5_lib.H5T_NATIVE_UINT, True)
    NATIVE_LONG = HDF5Type_(hdf5_lib.H5T_NATIVE_LONG, True)
    NATIVE_ULONG = HDF5Type_(hdf5_lib.H5T_NATIVE_ULONG, True)
    NATIVE_LLONG = HDF5Type_(hdf5_lib.H5T_NATIVE_LLONG, True)
    NATIVE_ULLONG = HDF5Type_(hdf5_lib.H5T_NATIVE_ULLONG, True)
    NATIVE_FLOAT = HDF5Type_(hdf5_lib.H5T_NATIVE_FLOAT, True)
    NATIVE_DOUBLE = HDF5Type_(hdf5_lib.H5T_NATIVE_DOUBLE, True)
    NATIVE_LDOUBLE = HDF5Type_(hdf5_lib.H5T_NATIVE_LDOUBLE, True)
    NATIVE_B8 = HDF5Type_(hdf5_lib.H5T_NATIVE_B8, True)
    NATIVE_B16 = HDF5Type_(hdf5_lib.H5T_NATIVE_B16, True)
    NATIVE_B32 = HDF5Type_(hdf5_lib.H5T_NATIVE_B32, True)
    NATIVE_B64 = HDF5Type_(hdf5_lib.H5T_NATIVE_B64, True)
    NATIVE_OPAQUE = HDF5Type_(hdf5_lib.H5T_NATIVE_OPAQUE, True)
    NATIVE_HADDR = HDF5Type_(hdf5_lib.H5T_NATIVE_HADDR, True)
    NATIVE_HSIZE = HDF5Type_(hdf5_lib.H5T_NATIVE_HSIZE, True)
    NATIVE_HSSIZE = HDF5Type_(hdf5_lib.H5T_NATIVE_HSSIZE, True)
    NATIVE_HERR = HDF5Type_(hdf5_lib.H5T_NATIVE_HERR, True)
    NATIVE_HBOOL = HDF5Type_(hdf5_lib.H5T_NATIVE_HBOOL, True)

    NATIVE_INT8 = HDF5Type_(hdf5_lib.H5T_NATIVE_INT8, True)
    NATIVE_UINT8 = HDF5Type_(hdf5_lib.H5T_NATIVE_UINT8, True)
    NATIVE_INT_LEAST8 = HDF5Type_(hdf5_lib.H5T_NATIVE_INT_LEAST8, True)
    NATIVE_UINT_LEAST8 = HDF5Type_(hdf5_lib.H5T_NATIVE_UINT_LEAST8, True)
    NATIVE_INT_FAST8 = HDF5Type_(hdf5_lib.H5T_NATIVE_INT_FAST8, True)
    NATIVE_UINT_FAST8 = HDF5Type_(hdf5_lib.H5T_NATIVE_UINT_FAST8, True)
    NATIVE_INT16 = HDF5Type_(hdf5_lib.H5T_NATIVE_INT16, True)
    NATIVE_UINT16 = HDF5Type_(hdf5_lib.H5T_NATIVE_UINT16, True)
    NATIVE_INT_LEAST16 = HDF5Type_(hdf5_lib.H5T_NATIVE_INT_LEAST16, True)
    NATIVE_UINT_LEAST16 = HDF5Type_(hdf5_lib.H5T_NATIVE_UINT_LEAST16, True)
    NATIVE_INT_FAST16 = HDF5Type_(hdf5_lib.H5T_NATIVE_INT_FAST16, True)
    NATIVE_UINT_FAST16 = HDF5Type_(hdf5_lib.H5T_NATIVE_UINT_FAST16, True)
    NATIVE_INT32 = HDF5Type_(hdf5_lib.H5T_NATIVE_INT32, True)
    NATIVE_UINT32 = HDF5Type_(hdf5_lib.H5T_NATIVE_UINT32, True)
    NATIVE_INT_LEAST32 = HDF5Type_(hdf5_lib.H5T_NATIVE_INT_LEAST32, True)
    NATIVE_UINT_LEAST32 = HDF5Type_(hdf5_lib.H5T_NATIVE_UINT_LEAST32, True)
    NATIVE_INT_FAST32 = HDF5Type_(hdf5_lib.H5T_NATIVE_INT_FAST32, True)
    NATIVE_UINT_FAST32 = HDF5Type_(hdf5_lib.H5T_NATIVE_UINT_FAST32, True)
    NATIVE_INT64 = HDF5Type_(hdf5_lib.H5T_NATIVE_INT64, True)
    NATIVE_UINT64 = HDF5Type_(hdf5_lib.H5T_NATIVE_UINT64, True)
    NATIVE_INT_LEAST64 = HDF5Type_(hdf5_lib.H5T_NATIVE_INT_LEAST64, True)
    NATIVE_UINT_LEAST64 = HDF5Type_(hdf5_lib.H5T_NATIVE_UINT_LEAST64, True)
    NATIVE_INT_FAST64 = HDF5Type_(hdf5_lib.H5T_NATIVE_INT_FAST64, True)
    NATIVE_UINT_FAST64 = HDF5Type_(hdf5_lib.H5T_NATIVE_UINT_FAST64, True)
