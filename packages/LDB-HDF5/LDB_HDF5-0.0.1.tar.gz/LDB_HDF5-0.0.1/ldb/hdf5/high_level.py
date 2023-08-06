from __future__ import absolute_import

from ldb.hdf5._hdf5 import lib as hdf5_lib, ffi as hdf5_ffi
from ldb.hdf5.low_level import (HDF5File_, HDF5Dataspace_, HDF5Dataset_,
                                HDF5Attribute_, HDF5Type_, HDF5TypeBuiltin_)
from ldb.hdf5.exceptions import DatasetExistsError, AttributeExistsError

import itertools
import numbers

# TODO: Check all pointers/array for proper size before using
# TODO: Need reference counting on enter/exit to avoid insanity, don't close
# until all contexts have exited

"""
This module provides a higher level abstraction of HDF5 objects.

Where the low level module provides an almost 1:1 mapping of functions to
classes, adding only the concept of context managers this module makes the
overall structure more pythonic. For instance, instead of doing
HDF5Dataset_.create2(hdf5_loc, ...) you do hdf5_loc.create_dataset(...). This
module also provides functionality to handle the management of in memory
datasets and converting between python, C and HDF5 datatypes.

All function calls to the HDF5 API should be performed through the low_level
module. However most/all of the use of constants are used directly from the
cffi module as the low_level module provides little/no abstraction of the
underlying constants.
"""

class HDF5Location(object):
    """
    This class is a mixin to provide methods that operate on locations (files,
    groups, etc). The class it is attached to must have a location property
    that provides a low level location. A low level location is anything that
    provides a loc_id property.
    """
    def create_dataset(self, dataset_name, datatype, dataspace,
                       link_creation_properties=None,
                       dataset_creation_properties=None,
                       dataset_access_properties=None,
                       fail_if_exists=False):
        try:
            dataset_ = HDF5Dataset_.create2(self.location, dataset_name,
                                            datatype.ll_type,
                                            dataspace.ll_dataspace,
                                            link_creation_properties,
                                            dataset_creation_properties,
                                            dataset_access_properties)
        except DatasetExistsError:
            if fail_if_exists:
                raise
            # TODO: Check dataset matches things like dataspace as appropriate
            dataset_ = HDF5Dataset_.open2(self.location, dataset_name,
                                          dataset_access_properties)
        return HDF5Dataset(dataset_)

    def open_dataset(self, dataset_name, dataset_access_properties=None):
        return HDF5Dataset(HDF5Dataset_.open2(self.location, dataset_name,
                                              dataset_access_properties))

    def create_attribute(self, attribute_name, datatype, dataspace,
                         attribute_creation_properties=None,
                         attribute_access_properties=None,
                         fail_if_exists=False):
        try:
            attr_ = HDF5Attribute_.create2(self.location, attribute_name,
                                           datatype.ll_type,
                                           dataspace.ll_dataspace,
                                           attribute_creation_properties,
                                           attribute_access_properties)
        except AttributeExistsError:
            if fail_if_exists:
                raise
            # TODO: Check dataset matches things like dataspace as appropriate
            attr_ = HDF5Attribute_.open(self.location, attribute_name,
                                        attribute_access_properties)
        return HDF5Attribute(attr_)

    def open_attribute(self, attribute_name, attribute_access_properties=None):
        attr_ = HDF5Attribute_.open(self.location, attribute_name,
                                    attribute_access_properties)
        return HDF5Attribute(attr_)


class HDF5File(HDF5Location):
    def __init__(self, ll_file):
        self.ll_file = ll_file

    @property
    def location(self):
        return self.ll_file

    @classmethod
    def open(cls, filename, read_only=False):
        if read_only:
            return cls(HDF5File_.open(filename, read_only))

        try:
            return cls(HDF5File_.create(filename, truncate_if_exists=False))
        except IOError:# TODO: py3.3 FileExistsError:
            # TODO: Reduce noisyness on create failure
            return cls(HDF5File_.open(filename, read_only))

    def flush(self, scope=hdf5_lib.H5F_SCOPE_LOCAL):
        self.ll_file.flush(scope)

    def __enter__(self):
        self.ll_file.__enter__()
        return self

    def __exit__(self, a, b, c):
        return self.ll_file.__exit__(a, b, c)


class HDF5Dataspace(object):
    def __init__(self, ll_dataspace):
        self.ll_dataspace = ll_dataspace

    @classmethod
    def create_scalar(cls):
        return cls(HDF5Dataspace_.create(hdf5_lib.H5S_SCALAR))

    @classmethod
    def create_simple(cls, current_dims, maximum_dims=None):
        return cls(HDF5Dataspace_.create_simple(current_dims, maximum_dims))

    @property
    def simple_extent_dims(self):
        ndims = self.ll_dataspace.get_simple_extent_ndims()
        dims = hdf5_ffi.new('hsize_t[%d]'%(ndims,))
        self.ll_dataspace.get_simple_extent_dims(dims)
        return dims

    @property
    def simple_extent_maximum_dims(self):
        ndims = self.ll_dataspace.get_simple_extent_ndims()
        maximum_dims = hdf5_ffi.new('hsize_t[%d]'%(ndims,))
        self.ll_dataspace.get_simple_extent_dims(None, maximum_dims)
        return maximum_dims

    def select_hyperslab(self, select_operator, start, stride, count,
                         block=None):
        return self.ll_dataspace.select_hyperslab(select_operator, start,
                                                  stride, count, block)

    def __enter__(self):
        self.ll_dataspace.__enter__()
        return self

    def __exit__(self, a, b, c):
        return self.ll_dataspace.__exit__(a, b, c)


# TODO: Better name than Data??
class DataContainer(object):
    def __init__(self, type_, size):
        # TODO: Take initializer
        type_class = type_.class_
        self.type_class = TypeClass.from_hdf5_type_class(type_class, type_)

        self.data = hdf5_ffi.new(self.type_class.c_array_type(size))
        self.size = size
        self.refs = []

    def __getitem__(self, key):
        data = self.data
        try:
            for idx in key:
                data = data[idx]
        # TODO: Make this except more specific
        except:
            data = data[key]
        return self.type_class.read_convert(data)

    def __setitem__(self, key, value):
        store_value = self.type_class.write_convert(value)
        if self.type_class.hold_ref:
            self.refs.append(store_value)

        array = self.data
        try:
            for idx in key[:-1]:
                array = array[idx]

            array[key[-1]] = store_value
        except:
            array[key] = store_value

    @property
    def indices(self):
        return itertools.product(*[range(size_) for size_ in self.size])


class HDF5Dataset(HDF5Location):
    def __init__(self, ll_dataset):
        self.ll_dataset = ll_dataset

    @property
    def location(self):
        return self.ll_dataset

    def _assert_scalar(self):
        assert len(self.space.simple_extent_dims) == 0

    @property
    def scalar(self):
        self._assert_scalar()

        type_class = TypeClass.from_hdf5_type_class(self.type_.class_,
                                                    self.type_)
        data = hdf5_ffi.new(type_class.c_array_type([1]))

        self.ll_dataset.read(type_class.hdf5_type.ll_type, data)

        return type_class.read_convert(data[0])

    @scalar.setter
    def scalar(self, value):
        self._assert_scalar()

        type_class = TypeClass.from_hdf5_type_class(self.type_.class_,
                                                    self.type_)
        data = hdf5_ffi.new(type_class.c_array_type([1]))
        data[0] = type_class.write_convert(value)

        self.ll_dataset.write(type_class.hdf5_type.ll_type, data)

    def __getitem__(self, key):
        if key == Ellipsis:
            data = self.make_data()
            self.ll_dataset.read(data.type_class.hdf5_type.ll_type, data.data)
        else:
            file_dataspace, mem_dataspace, count = self._make_dataspaces(key)

            if len(count) == 0:
                type_class = TypeClass.from_hdf5_type_class(self.type_.class_,
                                                            self.type_)
                data = hdf5_ffi.new(type_class.c_array_type([1]))

                self.ll_dataset.read(type_class.hdf5_type.ll_type, data,
                                     mem_dataspace.ll_dataspace,
                                     file_dataspace.ll_dataspace)

                return type_class.read_convert(data[0])

            data = DataContainer(self.type_, count)
            self.ll_dataset.read(data.type_class.hdf5_type.ll_type, data.data,
                                 mem_dataspace.ll_dataspace,
                                 file_dataspace.ll_dataspace)

        return data

    def __setitem__(self, key, value):
        if key == Ellipsis:
            self.ll_dataset.write(value.type_class.hdf5_type.ll_type,
                                  value.data)
        else:
            file_dataspace, mem_dataspace, count = self._make_dataspaces(key)

            if len(count) == 0:
                type_class = TypeClass.from_hdf5_type_class(self.type_.class_,
                                                            self.type_)
                data = hdf5_ffi.new(type_class.c_array_type([1]))
                data[0] = type_class.write_convert(value)

                self.ll_dataset.write(type_class.hdf5_type.ll_type, data,
                                      mem_dataspace.ll_dataspace,
                                      file_dataspace.ll_dataspace)

                return

            self.ll_dataset.write(value.type_class.hdf5_type.ll_type,
                                  value.data, mem_dataspace.ll_dataspace,
                                  file_dataspace.ll_dataspace)

    # TODO: Handle 1D key (i.e. dataset[0] as opposed to dataset[0,])
    def _make_dataspaces(self, key):
        dims = self.space.simple_extent_dims
        rank = len(dims)
        assert len(key) == rank

        start = [0]*rank
        stride = [1]*rank
        count = list(dims)
        use_dim = [True]*rank

        for i, (key_part, dim) in enumerate(zip(key, dims)):
            if isinstance(key_part, slice):
                # In python3 this would be range(dim)[key_part].start/step
                if key_part.start is not None:
                    start[i] = key_part.start
                if key_part.step is not None:
                    stride[i] = key_part.step
                count[i] = len(range(dim)[key_part])
            else:
                # Assume it's an integer index
                start[i] = key_part
                count[i] = 1
                use_dim[i] = False

        file_dataspace = HDF5Dataspace.create_simple(dims)
        file_dataspace.select_hyperslab(hdf5_lib.H5S_SELECT_SET, start,
                                        stride, count)
        mem_dataspace = HDF5Dataspace.create_simple(count)

        start = [_ for _, use in zip(start, use_dim) if use != 0]
        stride = [_ for _, use in zip(stride, use_dim) if use != 0]
        count = [_ for _, use in zip(count, use_dim) if use != 0]

        return file_dataspace, mem_dataspace, count

    @property
    def space(self):
        return HDF5Dataspace(self.ll_dataset.get_space())

    @property
    def type_(self):
        return HDF5Type.wrap(self.ll_dataset.get_type())

    def make_data(self, size=None):
        if size is None:
            size = self.space.simple_extent_dims
        type_ = self.type_
        return DataContainer(type_, size)

    def __enter__(self):
        self.ll_dataset.__enter__()
        return self

    def __exit__(self, a, b, c):
        return self.ll_dataset.__exit__(a, b, c)


class HDF5Attribute(object):
    def __init__(self, ll_attribute):
        self.ll_attribute = ll_attribute

    def _assert_scalar(self):
        assert len(self.space.simple_extent_dims) == 0

    @property
    def scalar(self):
        self._assert_scalar()

        type_class = TypeClass.from_hdf5_type_class(self.type_.class_,
                                                    self.type_)
        data = hdf5_ffi.new(type_class.c_array_type([1]))

        self.ll_attribute.read(type_class.hdf5_type.ll_type, data)

        return type_class.read_convert(data[0])

    @scalar.setter
    def scalar(self, value):
        self._assert_scalar()

        type_class = TypeClass.from_hdf5_type_class(self.type_.class_,
                                                    self.type_)
        data = hdf5_ffi.new(type_class.c_array_type([1]))
        data[0] = type_class.write_convert(value)

        self.ll_attribute.write(type_class.hdf5_type.ll_type, data)

    def __getitem__(self, key):
        if key == Ellipsis:
            data = self.make_data()
            self.ll_attribute.read(data.type_class.hdf5_type.ll_type,
                                   data.data)
            return data
        else:
            raise KeyError

    def __setitem__(self, key, value):
        if key == Ellipsis:
            self.ll_attribute.write(value.type_class.hdf5_type.ll_type,
                                    value.data)
        else:
            raise KeyError

    @property
    def space(self):
        return HDF5Dataspace(self.ll_attribute.get_space())

    @property
    def type_(self):
        return HDF5Type.wrap(self.ll_attribute.get_type())

    def make_data(self, size=None):
        if size is None:
            size = self.space.simple_extent_dims
        type_ = self.type_
        return DataContainer(type_, size)

    def __enter__(self):
        self.ll_attribute.__enter__()
        return self

    def __exit__(self, a, b, c):
        return self.ll_attribute.__exit__(a, b, c)


class HDF5Type(object):
    def __init__(self, ll_type):
        self.ll_type = ll_type

    @staticmethod
    def wrap(ll_type):
        type_class = ll_type.get_class()
        if type_class == hdf5_lib.H5T_COMPOUND:
            return HDF5TypeCompound(ll_type)
        else:
            return HDF5Type(ll_type)

    @classmethod
    def create(cls, class_, size):
        return cls(HDF5Type_.create(class_, size))

    def copy(self):
        return HDF5Type.wrap(self.ll_type.copy())

    @property
    def class_(self):
        return self.ll_type.get_class()

    @property
    def size(self):
        return self.ll_type.get_size()

    @size.setter
    def size(self, value):
        return self.ll_type.set_size(value)

    def __enter__(self):
        self.ll_type.__enter__()
        return self

    def __exit__(self, a, b, c):
        return self.ll_type.__exit__(a, b, c)


class HDF5TypeBuiltin(object):
    IEEE_F32BE = HDF5Type.wrap(HDF5TypeBuiltin_.IEEE_F32BE)
    IEEE_F32LE = HDF5Type.wrap(HDF5TypeBuiltin_.IEEE_F32LE)
    IEEE_F64BE = HDF5Type.wrap(HDF5TypeBuiltin_.IEEE_F64BE)
    IEEE_F64LE = HDF5Type.wrap(HDF5TypeBuiltin_.IEEE_F64LE)

    STD_I8BE = HDF5Type.wrap(HDF5TypeBuiltin_.STD_I8BE)
    STD_I8LE = HDF5Type.wrap(HDF5TypeBuiltin_.STD_I8LE)
    STD_I16BE = HDF5Type.wrap(HDF5TypeBuiltin_.STD_I16BE)
    STD_I16LE = HDF5Type.wrap(HDF5TypeBuiltin_.STD_I16LE)
    STD_I32BE = HDF5Type.wrap(HDF5TypeBuiltin_.STD_I32BE)
    STD_I32LE = HDF5Type.wrap(HDF5TypeBuiltin_.STD_I32LE)
    STD_I64BE = HDF5Type.wrap(HDF5TypeBuiltin_.STD_I64BE)
    STD_I64LE = HDF5Type.wrap(HDF5TypeBuiltin_.STD_I64LE)
    STD_U8BE = HDF5Type.wrap(HDF5TypeBuiltin_.STD_U8BE)
    STD_U8LE = HDF5Type.wrap(HDF5TypeBuiltin_.STD_U8LE)
    STD_U16BE = HDF5Type.wrap(HDF5TypeBuiltin_.STD_U16BE)
    STD_U16LE = HDF5Type.wrap(HDF5TypeBuiltin_.STD_U16LE)
    STD_U32BE = HDF5Type.wrap(HDF5TypeBuiltin_.STD_U32BE)
    STD_U32LE = HDF5Type.wrap(HDF5TypeBuiltin_.STD_U32LE)
    STD_U64BE = HDF5Type.wrap(HDF5TypeBuiltin_.STD_U64BE)
    STD_U64LE = HDF5Type.wrap(HDF5TypeBuiltin_.STD_U64LE)
    STD_B8BE = HDF5Type.wrap(HDF5TypeBuiltin_.STD_B8BE)
    STD_B8LE = HDF5Type.wrap(HDF5TypeBuiltin_.STD_B8LE)
    STD_B16BE = HDF5Type.wrap(HDF5TypeBuiltin_.STD_B16BE)
    STD_B16LE = HDF5Type.wrap(HDF5TypeBuiltin_.STD_B16LE)
    STD_B32BE = HDF5Type.wrap(HDF5TypeBuiltin_.STD_B32BE)
    STD_B32LE = HDF5Type.wrap(HDF5TypeBuiltin_.STD_B32LE)
    STD_B64BE = HDF5Type.wrap(HDF5TypeBuiltin_.STD_B64BE)
    STD_B64LE = HDF5Type.wrap(HDF5TypeBuiltin_.STD_B64LE)

    STD_REF_OBJ = HDF5Type.wrap(HDF5TypeBuiltin_.STD_REF_OBJ)
    STD_REF_DSETREG = HDF5Type.wrap(HDF5TypeBuiltin_.STD_REF_DSETREG)

    UNIX_D32BE = HDF5Type.wrap(HDF5TypeBuiltin_.UNIX_D32BE)
    UNIX_D32LE = HDF5Type.wrap(HDF5TypeBuiltin_.UNIX_D32LE)
    UNIX_D64BE = HDF5Type.wrap(HDF5TypeBuiltin_.UNIX_D64BE)
    UNIX_D64LE = HDF5Type.wrap(HDF5TypeBuiltin_.UNIX_D64LE)

    C_S1 = HDF5Type.wrap(HDF5TypeBuiltin_.C_S1)
    FORTRAN_S1 = HDF5Type.wrap(HDF5TypeBuiltin_.FORTRAN_S1)

    INTEL_I8 = HDF5Type.wrap(HDF5TypeBuiltin_.INTEL_I8)
    INTEL_I16 = HDF5Type.wrap(HDF5TypeBuiltin_.INTEL_I16)
    INTEL_I32 = HDF5Type.wrap(HDF5TypeBuiltin_.INTEL_I32)
    INTEL_I64 = HDF5Type.wrap(HDF5TypeBuiltin_.INTEL_I64)
    INTEL_U8 = HDF5Type.wrap(HDF5TypeBuiltin_.INTEL_U8)
    INTEL_U16 = HDF5Type.wrap(HDF5TypeBuiltin_.INTEL_U16)
    INTEL_U32 = HDF5Type.wrap(HDF5TypeBuiltin_.INTEL_U32)
    INTEL_U64 = HDF5Type.wrap(HDF5TypeBuiltin_.INTEL_U64)
    INTEL_B8 = HDF5Type.wrap(HDF5TypeBuiltin_.INTEL_B8)
    INTEL_B16 = HDF5Type.wrap(HDF5TypeBuiltin_.INTEL_B16)
    INTEL_B32 = HDF5Type.wrap(HDF5TypeBuiltin_.INTEL_B32)
    INTEL_B64 = HDF5Type.wrap(HDF5TypeBuiltin_.INTEL_B64)
    INTEL_F32 = HDF5Type.wrap(HDF5TypeBuiltin_.INTEL_F32)
    INTEL_F64 = HDF5Type.wrap(HDF5TypeBuiltin_.INTEL_F64)

    ALPHA_I8 = HDF5Type.wrap(HDF5TypeBuiltin_.ALPHA_I8)
    ALPHA_I16 = HDF5Type.wrap(HDF5TypeBuiltin_.ALPHA_I16)
    ALPHA_I32 = HDF5Type.wrap(HDF5TypeBuiltin_.ALPHA_I32)
    ALPHA_I64 = HDF5Type.wrap(HDF5TypeBuiltin_.ALPHA_I64)
    ALPHA_U8 = HDF5Type.wrap(HDF5TypeBuiltin_.ALPHA_U8)
    ALPHA_U16 = HDF5Type.wrap(HDF5TypeBuiltin_.ALPHA_U16)
    ALPHA_U32 = HDF5Type.wrap(HDF5TypeBuiltin_.ALPHA_U32)
    ALPHA_U64 = HDF5Type.wrap(HDF5TypeBuiltin_.ALPHA_U64)
    ALPHA_B8 = HDF5Type.wrap(HDF5TypeBuiltin_.ALPHA_B8)
    ALPHA_B16 = HDF5Type.wrap(HDF5TypeBuiltin_.ALPHA_B16)
    ALPHA_B32 = HDF5Type.wrap(HDF5TypeBuiltin_.ALPHA_B32)
    ALPHA_B64 = HDF5Type.wrap(HDF5TypeBuiltin_.ALPHA_B64)
    ALPHA_F32 = HDF5Type.wrap(HDF5TypeBuiltin_.ALPHA_F32)
    ALPHA_F64 = HDF5Type.wrap(HDF5TypeBuiltin_.ALPHA_F64)

    MIPS_I8 = HDF5Type.wrap(HDF5TypeBuiltin_.MIPS_I8)
    MIPS_I16 = HDF5Type.wrap(HDF5TypeBuiltin_.MIPS_I16)
    MIPS_I32 = HDF5Type.wrap(HDF5TypeBuiltin_.MIPS_I32)
    MIPS_I64 = HDF5Type.wrap(HDF5TypeBuiltin_.MIPS_I64)
    MIPS_U8 = HDF5Type.wrap(HDF5TypeBuiltin_.MIPS_U8)
    MIPS_U16 = HDF5Type.wrap(HDF5TypeBuiltin_.MIPS_U16)
    MIPS_U32 = HDF5Type.wrap(HDF5TypeBuiltin_.MIPS_U32)
    MIPS_U64 = HDF5Type.wrap(HDF5TypeBuiltin_.MIPS_U64)
    MIPS_B8 = HDF5Type.wrap(HDF5TypeBuiltin_.MIPS_B8)
    MIPS_B16 = HDF5Type.wrap(HDF5TypeBuiltin_.MIPS_B16)
    MIPS_B32 = HDF5Type.wrap(HDF5TypeBuiltin_.MIPS_B32)
    MIPS_B64 = HDF5Type.wrap(HDF5TypeBuiltin_.MIPS_B64)
    MIPS_F32 = HDF5Type.wrap(HDF5TypeBuiltin_.MIPS_F32)
    MIPS_F64 = HDF5Type.wrap(HDF5TypeBuiltin_.MIPS_F64)

    VAX_F32 = HDF5Type.wrap(HDF5TypeBuiltin_.VAX_F32)
    VAX_F64 = HDF5Type.wrap(HDF5TypeBuiltin_.VAX_F64)

    NATIVE_CHAR = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_CHAR)
    NATIVE_SCHAR = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_SCHAR)
    NATIVE_UCHAR = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_UCHAR)
    NATIVE_SHORT = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_SHORT)
    NATIVE_USHORT = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_USHORT)
    NATIVE_INT = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_INT)
    NATIVE_UINT = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_UINT)
    NATIVE_LONG = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_LONG)
    NATIVE_ULONG = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_ULONG)
    NATIVE_LLONG = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_LLONG)
    NATIVE_ULLONG = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_ULLONG)
    NATIVE_FLOAT = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_FLOAT)
    NATIVE_DOUBLE = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_DOUBLE)
    NATIVE_LDOUBLE = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_LDOUBLE)
    NATIVE_B8 = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_B8)
    NATIVE_B16 = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_B16)
    NATIVE_B32 = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_B32)
    NATIVE_B64 = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_B64)
    NATIVE_OPAQUE = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_OPAQUE)
    NATIVE_HADDR = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_HADDR)
    NATIVE_HSIZE = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_HSIZE)
    NATIVE_HSSIZE = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_HSSIZE)
    NATIVE_HERR = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_HERR)
    NATIVE_HBOOL = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_HBOOL)

    NATIVE_INT8 = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_INT8)
    NATIVE_UINT8 = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_UINT8)
    NATIVE_INT_LEAST8 = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_INT_LEAST8)
    NATIVE_UINT_LEAST8 = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_UINT_LEAST8)
    NATIVE_INT_FAST8 = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_INT_FAST8)
    NATIVE_UINT_FAST8 = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_UINT_FAST8)
    NATIVE_INT16 = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_INT16)
    NATIVE_UINT16 = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_UINT16)
    NATIVE_INT_LEAST16 = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_INT_LEAST16)
    NATIVE_UINT_LEAST16 = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_UINT_LEAST16)
    NATIVE_INT_FAST16 = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_INT_FAST16)
    NATIVE_UINT_FAST16 = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_UINT_FAST16)
    NATIVE_INT32 = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_INT32)
    NATIVE_UINT32 = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_UINT32)
    NATIVE_INT_LEAST32 = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_INT_LEAST32)
    NATIVE_UINT_LEAST32 = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_UINT_LEAST32)
    NATIVE_INT_FAST32 = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_INT_FAST32)
    NATIVE_UINT_FAST32 = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_UINT_FAST32)
    NATIVE_INT64 = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_INT64)
    NATIVE_UINT64 = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_UINT64)
    NATIVE_INT_LEAST64 = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_INT_LEAST64)
    NATIVE_UINT_LEAST64 = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_UINT_LEAST64)
    NATIVE_INT_FAST64 = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_INT_FAST64)
    NATIVE_UINT_FAST64 = HDF5Type.wrap(HDF5TypeBuiltin_.NATIVE_UINT_FAST64)


class HDF5TypeCompound(HDF5Type):
    @classmethod
    def create_compound(cls, members):
        """
        members - a sequence with each element being of the form
            [member_name, type]
        """
        # TODO: Handle variable length strings...
        offset = 0
        members_ = []
        for member in members:
            member = list(member)
            member.append(offset)
            offset += member[1].size
            members_.append(member)

        type_ = cls.create(hdf5_lib.H5T_COMPOUND, offset)

        for member in members_:
            type_.insert(member[0], member[2], member[1])

        return type_

    # TODO: Represent members as a class and return a list of these classes
    # instead
    def get_member_class(self, member_no):
        return self.ll_type.get_member_class(member_no)

    def get_member_index(self, field_name):
        return self.ll_type.get_member_index(field_name)

    def get_member_name(self, field_idx):
        return self.ll_type.get_member_name(field_idx)

    def get_member_offset(self, memb_no):
        return self.ll_type.get_member_offset(memb_no)

    def get_member_type(self, field_idx):
        return HDF5Type.wrap(self.ll_type.get_member_type(field_idx))

    @property
    def num_members(self):
        return self.ll_type.get_nmembers()

    def insert(self, name, offset, field_id):
        self.ll_type.insert(name, offset, field_id.ll_type)


variable_c_str_type = HDF5TypeBuiltin.C_S1.copy()
variable_c_str_type.size = hdf5_lib.H5T_VARIABLE


# TODO: Either put in preferred file types here (like fortran string) or figure
# out where to put that
class TypeClass(object):
    def __init__(self, c_type, hdf5_type, read_convert, write_convert,
                 hold_ref):
        # TODO: Strings need variable length formatting on mem side (custom
        # type copy of C_S1
        self.c_type = c_type
        self.c_type_array_size = None
        self.hdf5_type = hdf5_type
        self.read_convert = read_convert
        self.write_convert = write_convert
        self.hold_ref = hold_ref

    @classmethod
    def guess_type_class(cls, python_value):
        if isinstance(python_value, bool):
            return cls.from_hdf5_type_class(hdf5_lib.H5T_INTEGER)
        elif isinstance(python_value, numbers.Integral):
            return cls.from_hdf5_type_class(hdf5_lib.H5T_INTEGER)
        elif isinstance(python_value, numbers.Real):
            return cls.from_hdf5_type_class(hdf5_lib.H5T_FLOAT)
        else:
            return cls.from_hdf5_type_class(hdf5_lib.H5T_STRING)

    @classmethod
    def from_hdf5_type_class(cls, type_class, type_=None):
        """
        type_ - required for H5T_COMPOUND objects
        """
        type_class_dict = {
            hdf5_lib.H5T_INTEGER: ('int', HDF5TypeBuiltin.NATIVE_INT,
                                   lambda x: x, lambda x: x, False),
            hdf5_lib.H5T_FLOAT: ('double', HDF5TypeBuiltin.NATIVE_DOUBLE,
                                 lambda x: x, lambda x: x, False),
            # TODO: Reclaim memory on read using H5Dvlen_reclaim to avoid memory leak
            hdf5_lib.H5T_STRING: ('char*', variable_c_str_type,
                                  lambda x: hdf5_ffi.string(x).decode("utf8"),
                                  lambda x: hdf5_ffi.new('char[]',
                                                         x.encode("utf8")),
                                  True),
        }
        if type_class == hdf5_lib.H5T_COMPOUND:
            return TypeClassCompound(type_)
        return cls(*type_class_dict[type_class])

    def c_array_type(self, size):
        c_full_type = '%s[%s]'%(self.c_type,
                                ']['.join(map(lambda x: "%d"%(int(x)), size)))
        if self.c_type_array_size is not None:
            c_full_type += '[%d]'%(self.c_type_array_size)
        return c_full_type


class PythonCompoundObject(object):
    pass

class TypeClassCompound(TypeClass):
    def __init__(self, type_compound):
        self.c_type = 'char'
        self.c_type_array_size = type_compound.size
        self.hold_ref = True

        self.original_type = type_compound
        self.members = []
        for i in range(type_compound.num_members):
            type_class = type_compound.get_member_class(i)
            type_ = type_compound.get_member_type(i)
            member = [type_compound.get_member_name(i),
                      TypeClass.from_hdf5_type_class(type_class, type_),
                     ]
            self.members.append(member)

        members2 = [(a, type_class.hdf5_type)
                    for a, type_class in self.members]
        self.hdf5_type = HDF5TypeCompound.create_compound(members2)

    def read_convert(self, value):
        value_binary = hdf5_ffi.buffer(value)
        result_inst = PythonCompoundObject()
        for member_name, member_type_class in self.members:
            size = member_type_class.hdf5_type.size
            member_binary = value_binary[:size]
            value_binary = value_binary[size:]
            member_cffi_blind_value = hdf5_ffi.from_buffer(member_binary)
            member_cffi_value = hdf5_ffi.cast('%s*'%(member_type_class.c_type),
                                              member_cffi_blind_value)[0]
            member_converted_value = member_type_class.read_convert(
                member_cffi_value)
            setattr(result_inst, member_name, member_converted_value)

        return result_inst

    def write_convert(self, value):
        result_binary = b''
        for member in self.members:
            member_value = getattr(value, member[0])
            # TODO: Where to hold values?
            member_converted_value = member[1].write_convert(member_value)
            member_cffi_value = hdf5_ffi.new('%s*'%(member[1].c_type,),
                                             member_converted_value)
            binary_value = bytes(hdf5_ffi.buffer(member_cffi_value))
            result_binary += binary_value
        return result_binary
