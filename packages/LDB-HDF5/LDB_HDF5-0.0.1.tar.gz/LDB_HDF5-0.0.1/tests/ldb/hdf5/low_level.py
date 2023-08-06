from __future__ import absolute_import

import unittest
import os

from ldb.hdf5._hdf5 import lib, ffi
from ldb.hdf5.low_level import (HDF5File_, HDF5Dataspace_, HDF5Dataset_,
                                HDF5Attribute_, HDF5Type_, HDF5TypeBuiltin_)
from ldb.hdf5.exceptions import DatasetExistsError, AttributeExistsError

import tests

import struct

hdf5_std_i32be = HDF5TypeBuiltin_.STD_I32BE

def create_dataset(file_, dataset_name='dset'):
    with HDF5Dataspace_.create_simple([10, 10]) as dataspace:
        with HDF5Dataset_.create2(file_, dataset_name, hdf5_std_i32be,
                                  dataspace) as dataset:
            data = ffi.new('int[10][10]')
            for i, a in enumerate(data):
                for j, b in enumerate(a):
                    a[j] = i*100 + j

            dataset.write(HDF5TypeBuiltin_.NATIVE_INT, data)


def create_attribute(file_, dataset_name='dset', attr_name='attr'):
    with HDF5Dataset_.open2(file_, dataset_name) as dataset:
        with HDF5Dataspace_.create_simple([4]) as dataspace:
            filetype = HDF5TypeBuiltin_.FORTRAN_S1.copy()
            memtype = HDF5TypeBuiltin_.C_S1.copy()
            filetype.set_size(lib.H5T_VARIABLE)
            memtype.set_size(lib.H5T_VARIABLE)

            with HDF5Attribute_.create2(dataset, attr_name, filetype,
                                        dataspace) as attr:
                strings = [ffi.new('char[]', b'Test'),
                           ffi.new('char[]', b'me'),
                           ffi.new('char[]', b''),
                           ffi.new('char[]', b'much')]
                data = ffi.new('char*[]', strings)

                attr.write(memtype, data)


class BasicTestCase(tests.CleanupMixin, unittest.TestCase):
    def setUp(self):
        super(BasicTestCase, self).setUp()
        filename = os.path.join(self.save_dir, 'test_%s.h5'%(self.id()))
        self.file = HDF5File_.create(filename, True)
        self.file.__enter__()

    def tearDown(self):
        self.file.__exit__(None, None, None)
        self.file = None
        super(BasicTestCase, self).tearDown()

class OtherTestCase(BasicTestCase):
    def testA(self):
        create_dataset(self.file)

        data = ffi.new('int[10][10]')
        dims = ffi.new('hsize_t[2]')

        with HDF5Dataset_.open2(self.file, 'dset') as dataset:
            dataspace = dataset.get_space()
            self.assertEqual(dataspace.get_simple_extent_ndims(), 2)

            dataspace.get_simple_extent_dims(dims)
            self.assertSequenceEqual(dims, [10, 10])

            dataset.read(HDF5TypeBuiltin_.NATIVE_INT, data)

        for i, a in enumerate(data):
            for j, b in enumerate(a):
                self.assertEqual(b, i*100 + j)

    def testB(self):
        create_dataset(self.file)
        create_attribute(self.file)

        data = ffi.new('char*[4]')
        dims = ffi.new('hsize_t[1]')
        expected_str = [b'Test', b'me', b'', b'much']

        with HDF5Dataset_.open2(self.file, 'dset') as dataset:
            with HDF5Attribute_.open(dataset, 'attr') as attr:
                dataspace = attr.get_space()
                self.assertEqual(dataspace.get_simple_extent_ndims(), 1)

                dataspace.get_simple_extent_dims(dims)
                self.assertSequenceEqual(dims, [4])

                memtype = lib.H5Tcopy(lib.H5T_C_S1)
                lib.H5Tset_size(memtype, lib.H5T_VARIABLE)
                memtype = HDF5Type_(memtype)
                attr.read(memtype, data)

        for c_str, exp_str in zip(data, expected_str):
            self.assertEqual(ffi.string(c_str), exp_str)

        self.file.flush(lib.H5F_SCOPE_LOCAL)


class HDF5File_TestCase(tests.CleanupMixin, unittest.TestCase):
    def testFileExistsThrows(self):
        filename = os.path.join(self.save_dir, 'test_%s.h5'%(self.id()))
        with HDF5File_.create(filename, True):
            pass

        with self.assertRaises(IOError):
            with HDF5File_.create(filename, False):
                pass

    def testFileOpen(self):
        with self.assertRaises(IOError):
            with HDF5File_.open('tests/does_not_exist'):
                pass

        with HDF5File_.open('tests/test_1.h5') as hdf5_file:
            data = ffi.new('int[10][10]')
            dims = ffi.new('hsize_t[2]')

            with HDF5Dataset_.open2(hdf5_file, 'dset') as dataset:
                dataspace = dataset.get_space()
                self.assertEqual(dataspace.get_simple_extent_ndims(), 2)

                dataspace.get_simple_extent_dims(dims)
                self.assertSequenceEqual(dims, [10, 10])

                dataset.read(HDF5TypeBuiltin_.NATIVE_INT, data)

            for i, a in enumerate(data):
                for j, b in enumerate(a):
                    self.assertEqual(b, i*100 + j)

        # TODO: Test writing fails, probably need error handling for this
        # anyway
        with HDF5File_.open('tests/test_1.h5', True) as hdf5_file:
            data = ffi.new('int[10][10]')
            dims = ffi.new('hsize_t[2]')

            with HDF5Dataset_.open2(hdf5_file, 'dset') as dataset:
                dataspace = dataset.get_space()
                self.assertEqual(dataspace.get_simple_extent_ndims(), 2)

                dataspace.get_simple_extent_dims(dims)
                self.assertSequenceEqual(dims, [10, 10])

                dataset.read(HDF5TypeBuiltin_.NATIVE_INT, data)

            for i, a in enumerate(data):
                for j, b in enumerate(a):
                    self.assertEqual(b, i*100 + j)

    def testMultipleContextEntry(self):
        filename = os.path.join(self.save_dir, 'test_%s.h5'%(self.id()))
        with HDF5File_.create(filename, True) as hdf5_file:
            with hdf5_file as hdf5_file2:
                self.assertEqual(hdf5_file, hdf5_file2)


class HDF5Dataspace_TestCase(unittest.TestCase):
    def setUp(self):
        self.dataspace = HDF5Dataspace_.create_simple([3,4], [5,6]).__enter__()

    def tearDown(self):
        self.dataspace.__exit__(None, None, None)
        self.dataspace = None

    def testCreateSimple(self):
        with HDF5Dataspace_.create_simple([3,4], [5,6]) as dataspace:
            dims = ffi.new('hsize_t[2]')
            max_dims = ffi.new('hsize_t[2]')
            lib.H5Sget_simple_extent_dims(dataspace.dataspace_id, dims,
                                          max_dims)
            self.assertSequenceEqual([3,4], dims)
            self.assertSequenceEqual([5,6], max_dims)

    def testGetSimpleExtentDims(self):
        dims = ffi.new('hsize_t[2]')
        self.dataspace.get_simple_extent_dims(dims)
        self.assertSequenceEqual([3,4], dims)

        max_dims = ffi.new('hsize_t[2]')
        self.dataspace.get_simple_extent_dims(None, max_dims)
        self.assertSequenceEqual([5,6], max_dims)

        dims = ffi.new('hsize_t[2]')
        max_dims = ffi.new('hsize_t[2]')
        self.dataspace.get_simple_extent_dims(dims, max_dims)
        self.assertSequenceEqual([3,4], dims)
        self.assertSequenceEqual([5,6], max_dims)

    def testCoverSelectHyperslab(self):
        self.dataspace.select_hyperslab(lib.H5S_SELECT_SET, [0,0], None, [1,1],
                                        [2,2])

class HDF5Dataset_TestCast(BasicTestCase):
    def testCreateExistingFails(self):
        dataset_name = 'dset'

        with HDF5Dataspace_.create_simple([10, 10]) as dataspace:
            with HDF5Dataset_.create2(self.file, dataset_name,
                                      hdf5_std_i32be,
                                      dataspace) as dataset:
                pass
            with self.assertRaises(DatasetExistsError):
                with HDF5Dataset_.create2(self.file, dataset_name,
                                          hdf5_std_i32be,
                                          dataspace) as dataset:
                    pass

class HDF5Attribute_TestCast(BasicTestCase):
    def testCreateExistingFails(self):
        dataset_name = 'dset'
        attr_name = 'attr'

        with HDF5Dataspace_.create_simple([10, 10]) as dataspace:
            with HDF5Dataset_.create2(self.file, dataset_name,
                                      hdf5_std_i32be,
                                      dataspace) as dataset:
                filetype = lib.H5Tcopy(lib.H5T_FORTRAN_S1)
                memtype = lib.H5Tcopy(lib.H5T_C_S1)
                lib.H5Tset_size(filetype, lib.H5T_VARIABLE)
                lib.H5Tset_size(memtype, lib.H5T_VARIABLE)
                filetype = HDF5Type_(filetype)
                memtype = HDF5Type_(memtype)

                with HDF5Attribute_.create2(dataset, attr_name, filetype,
                                            dataspace) as attr:
                    pass
                with self.assertRaises(AttributeExistsError):
                    with HDF5Attribute_.create2(dataset, attr_name,
                                                filetype,
                                                dataspace) as attr:
                        pass


class HDF5Type_TestCase(BasicTestCase):
    def testCreateType(self):
        with HDF5Type_.create(lib.H5T_COMPOUND, 13) as type_:
            self.assertEqual(lib.H5Tget_class(type_.type_id), lib.H5T_COMPOUND)
            self.assertEqual(lib.H5Tget_size(type_.type_id), 13)

            self.assertEqual(type_.get_class(), lib.H5T_COMPOUND)
            self.assertEqual(type_.get_size(), 13)

    def testInsert(self):
        my_struct = struct.Struct('>iqb')
        dataset_name = 'dset'

        with HDF5Type_.create(lib.H5T_COMPOUND, 13) as type_:
            type_.insert("asdf", 0, HDF5TypeBuiltin_.STD_I32BE)
            type_.insert("fdsa", 4, HDF5TypeBuiltin_.STD_I64BE)
            type_.insert("qwer", 12, HDF5TypeBuiltin_.STD_I8BE)

            self.assertEqual(type_.get_nmembers(), 3)
            self.assertEqual(type_.get_member_class(0), lib.H5T_INTEGER)
            self.assertEqual(type_.get_member_index("fdsa"), 1)
            self.assertEqual(type_.get_member_name(2), "qwer")
            self.assertEqual(type_.get_member_offset(1), 4)
            self.assertEqual(type_.get_member_type(2).get_size(), 1)

            with HDF5Dataspace_.create_simple([2]) as dataspace:
                with HDF5Dataset_.create2(self.file, dataset_name, type_,
                                          dataspace) as dataset:
                    data = ffi.new('char[2][13]', [my_struct.pack(1,2,3),
                                                   my_struct.pack(4,5,6)])

                    dataset.write(type_, data)


        with HDF5Type_.create(lib.H5T_COMPOUND, 8) as type_:
            type_.insert("fdsa", 0, HDF5TypeBuiltin_.NATIVE_INT64)

            with HDF5Dataset_.open2(self.file, dataset_name) as dataset:
                data = ffi.new('int64_t[2]')

                dataset.read(type_, data)

        self.assertSequenceEqual(data, [2, 5])

    def testContextFail(self):
        with self.assertRaises(Exception):
            with HDF5TypeBuiltin_.NATIVE_INT as test:
                pass
