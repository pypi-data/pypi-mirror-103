from __future__ import absolute_import

import unittest

from ldb.hdf5.high_level import (HDF5File, HDF5Dataspace, HDF5Dataset,
                                 HDF5Attribute, HDF5Type, TypeClass,
                                 HDF5TypeBuiltin, HDF5TypeCompound)

from ldb.hdf5._hdf5 import lib, ffi
from ldb.hdf5.low_level import HDF5Type_
from ldb.hdf5.exceptions import DatasetExistsError, AttributeExistsError

import tests

import os

hdf5_std_i32be = HDF5TypeBuiltin.STD_I32BE

def create_dataset(file_, dataset_name='dset'):
    with HDF5Dataspace.create_simple([10, 10]) as dataspace:
        with file_.create_dataset(dataset_name, hdf5_std_i32be,
                                  dataspace) as dataset:
            data = dataset.make_data()
            for i, j in data.indices:
                data[i, j] = i*100 + j

            dataset[...] = data


def create_attribute(file_, dataset_name='dset', attr_name='attr'):
    with file_.open_dataset(dataset_name) as dataset:
        with HDF5Dataspace.create_simple([4]) as dataspace:
            # TODO: Make this all high_level-ee
            filetype = HDF5TypeBuiltin.FORTRAN_S1.copy()
            filetype.size = lib.H5T_VARIABLE

            with dataset.create_attribute(attr_name, filetype,
                                          dataspace) as attr:
                data = attr.make_data()
                strings = ['Test', 'me', '', 'much']
                for i, str_ in enumerate(strings):
                    data[i] = str_

                attr[...] = data


class BasicTestCase(tests.CleanupMixin, unittest.TestCase):
    def setUp(self):
        super(BasicTestCase, self).setUp()
        # TODO: Use temporary files instead of this hack
        filename = os.path.join(self.save_dir, 'test_%s.h5'%(self.id()))
        try:
            os.remove(filename)
        except OSError:
            # Didn't exist, who cares
            pass
        self.file = HDF5File.open(filename)
        self.file.__enter__()

    def tearDown(self):
        self.file.__exit__(None, None, None)
        self.file = None
        super(BasicTestCase, self).tearDown()


class HDF5LocationTestCase(BasicTestCase):
    def setUp(self):
        super(HDF5LocationTestCase, self).setUp()
        create_dataset(self.file)

    def testCreateDatasetExists(self):
        dataset_name = 'dset'
        with HDF5Dataspace.create_simple([10, 10]) as dataspace:
            with self.file.create_dataset(dataset_name, hdf5_std_i32be,
                                          dataspace) as dataset:
                pass

            with self.assertRaises(DatasetExistsError):
                with self.file.create_dataset(dataset_name, hdf5_std_i32be,
                                              dataspace,
                                              fail_if_exists=True) as dataset:
                    pass

    def testCreateAttributeExists(self):
        create_dataset(self.file)
        dataset_name = 'dset'
        attr_name = 'attr'
        with self.file.open_dataset(dataset_name) as dataset:
            with HDF5Dataspace.create_simple([4]) as dataspace:
                # TODO: Make this all high_level-ee
                filetype = HDF5TypeBuiltin.FORTRAN_S1.copy()
                filetype.size = lib.H5T_VARIABLE

                with dataset.create_attribute(attr_name, filetype,
                                              dataspace) as attr:
                    pass

                with dataset.create_attribute(attr_name, filetype,
                                              dataspace) as attr:
                    dims = attr.space.simple_extent_dims
                    self.assertSequenceEqual(dims, [4])

                with self.assertRaises(AttributeExistsError):
                    with dataset.create_attribute(attr_name, filetype,
                                                  dataspace,
                                                  fail_if_exists=True) as attr:
                        pass


class HDF5FileTestCase(unittest.TestCase):
    def testOpen(self):
        with self.assertRaises(IOError):
            with HDF5File.open('tests/does_not_exist', True):
                pass

        with HDF5File.open('tests/test_1.h5') as hdf5_file:
            with hdf5_file.open_dataset('dset') as dataset:
                data = dataset[...]

            for i, j in data.indices:
                self.assertEqual(data[i, j], i*100 + j)

        # TODO: Test writing fails, probably need error handling for this
        # anyway
        with HDF5File.open('tests/test_1.h5', True) as hdf5_file:
            with hdf5_file.open_dataset('dset') as dataset:
                data = dataset[...]

            for i, j in data.indices:
                self.assertEqual(data[i, j], i*100 + j)


class HDF5DataspaceTestCase(unittest.TestCase):
    def testMakeDataspace(self):
        with HDF5Dataspace.create_simple([10, 10]) as dataspace:
            ll_dataspace = dataspace.ll_dataspace
            dims = ffi.new('hsize_t[2]')
            maximum_dims = ffi.new('hsize_t[2]')
            ll_dataspace.get_simple_extent_dims(dims, maximum_dims)
            self.assertSequenceEqual(dims, [10, 10])
            self.assertSequenceEqual(maximum_dims, [10, 10])

            self.assertSequenceEqual(dataspace.simple_extent_dims, [10, 10])
            self.assertSequenceEqual(dataspace.simple_extent_maximum_dims,
                                     [10, 10])

        with HDF5Dataspace.create_simple([10, 10], [12, 12]) as dataspace:
            ll_dataspace = dataspace.ll_dataspace
            dims = ffi.new('hsize_t[2]')
            maximum_dims = ffi.new('hsize_t[2]')
            ll_dataspace.get_simple_extent_dims(dims, maximum_dims)
            self.assertSequenceEqual(dims, [10, 10])
            self.assertSequenceEqual(maximum_dims, [12, 12])

            self.assertSequenceEqual(dataspace.simple_extent_dims, [10, 10])
            self.assertSequenceEqual(dataspace.simple_extent_maximum_dims,
                                     [12, 12])


class DataTestCase(unittest.TestCase):
    pass


class HDF5DatasetTestCase(BasicTestCase):
    def testDatasetScalar(self):
        create_dataset(self.file)

        with HDF5Dataspace.create_scalar() as dataspace:
            with self.file.create_dataset("test_scalar", hdf5_std_i32be,
                                          dataspace) as dataset:
                dataset.scalar = 31

        with self.file.open_dataset('test_scalar') as dataset:
            self.assertEqual(dataset.scalar, 31)

    def testCreateDataset(self):
        create_dataset(self.file)

        data = ffi.new('int[10][10]')

        with self.file.open_dataset('dset') as dataset:
            dataspace = dataset.space
            self.assertSequenceEqual(dataspace.simple_extent_dims, [10, 10])

            data = dataset[...]

        self.assertSequenceEqual(data.size, [10, 10])

        for i, j in data.indices:
            self.assertEqual(data[i, j], i*100 + j)

        self.file.flush()

    def testSubscriptDatasetGetSet(self):
        create_dataset(self.file)

        data = ffi.new('int[10][10]')

        with self.file.open_dataset('dset') as dataset:
            self.assertEqual(dataset[2, 3], 203)
            dataset[2,3] = 42
            self.assertEqual(dataset[2, 3], 42)

            dataspace = dataset.space
            self.assertSequenceEqual(dataspace.simple_extent_dims, [10, 10])

            data = dataset[...]

        self.assertSequenceEqual(data.size, [10, 10])

        for i, j in data.indices:
            if i == 2 and j == 3:
                self.assertEqual(data[i, j], 42)
            else:
                self.assertEqual(data[i, j], i*100 + j)

        with self.file.open_dataset('dset') as dataset:
            data = dataset[1:4:2, 2:6:3]

        for i, j in data.indices:
            self.assertEqual(data[i, j], (1+2*i)*100 + (2+3*j))

        with self.file.open_dataset('dset') as dataset:
            data = dataset.make_data([2,2])
            data[0,0] = 5
            data[0,1] = 6
            data[1,0] = 7
            data[1,1] = 8
            dataset[2:5:2, 1:4:2] = data

            data = dataset[...]

        self.assertSequenceEqual(data.size, [10, 10])

        for i, j in data.indices:
            if [i, j] in [[2,1], [2,3], [4,1], [4,3]]:
                self.assertEqual(data[i, j], 5+(i-2) + (j-1)/2)
            else:
                self.assertEqual(data[i, j], i*100 + j)

        # TODO: Test set slicing


class HDF5AttributeTestCase(BasicTestCase):
    def testCreateAttribute(self):
        create_dataset(self.file)
        create_attribute(self.file)

        expected_str = ['Test', 'me', '', 'much']

        with self.file.open_dataset('dset') as dataset:
            with dataset.open_attribute('attr') as attr:
                dataspace = attr.space
                self.assertSequenceEqual(dataspace.simple_extent_dims, [4])

                data = attr[...]

                with self.assertRaises(KeyError):
                    attr[1] = 1

                with self.assertRaises(KeyError):
                    attr[1]

        for str_, exp_str in zip(data, expected_str):
            self.assertEqual(str_, exp_str)

    def testAttributeScalar(self):
        create_dataset(self.file)

        with self.file.open_dataset('dset') as dataset:
            with HDF5Dataspace.create_scalar() as dataspace:
                with dataset.create_attribute("test_scalar", hdf5_std_i32be,
                                              dataspace) as attr:
                    attr.scalar = 31

        with self.file.open_dataset('dset') as dataset:
            with dataset.open_attribute("test_scalar") as attr:
                self.assertEqual(attr.scalar, 31)


class HDF5TypeTestCase(unittest.TestCase):
    def testCreateType(self):
        with HDF5Type.create(lib.H5T_COMPOUND, 13) as type_:
            self.assertEqual(type_.ll_type.get_class(), lib.H5T_COMPOUND)
            self.assertEqual(type_.ll_type.get_size(), 13)

            self.assertEqual(type_.class_, lib.H5T_COMPOUND)
            self.assertEqual(type_.size, 13)


class DummyObject(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

class HDF5TypeCompoudTestCase(BasicTestCase):
    def testCreateCompound(self):
        # TODO: Test this works with scalars/slices/etc
        members = [['a', HDF5TypeBuiltin.NATIVE_INT],
                   ['b', HDF5TypeBuiltin.NATIVE_DOUBLE]]
        with HDF5TypeCompound.create_compound(members) as type_:
            self.assertEqual(type_.num_members, 2)
            self.assertEqual(type_.get_member_class(0), lib.H5T_INTEGER)
            self.assertEqual(type_.get_member_index('b'), 1)
            self.assertEqual(type_.get_member_name(0), 'a')
            self.assertEqual(type_.get_member_offset(1),
                             HDF5TypeBuiltin.NATIVE_INT.size)
            self.assertEqual(type_.get_member_type(1).size,
                             HDF5TypeBuiltin.NATIVE_DOUBLE.size)

            with HDF5Dataspace.create_simple([2]) as dataspace, \
                    self.file.create_dataset('dset', type_,
                                             dataspace) as dataset:
                data = dataset.make_data()
                data[0] = DummyObject(13, 42.0)
                data[1] = DummyObject(7, 32.0)
                dataset[...] = data

        with self.file.open_dataset('dset') as dataset:
            self.assertEqual(dataset[0,].a, 13)
            self.assertEqual(dataset[0,].b, 42.0)
            self.assertEqual(dataset[1,].a, 7)
            self.assertEqual(dataset[1,].b, 32.0)


class TypeClassTestCase(unittest.TestCase):
    def testGuessTypeClass(self):
        self.assertEqual(TypeClass.guess_type_class(True).hdf5_type.class_,
                         lib.H5T_INTEGER)
        type_class = TypeClass.guess_type_class(42)
        self.assertEqual(type_class.hdf5_type.class_, lib.H5T_INTEGER)

        type_class = TypeClass.guess_type_class(42.0)
        self.assertEqual(type_class.hdf5_type.class_, lib.H5T_FLOAT)

        type_class = TypeClass.guess_type_class('42')
        self.assertEqual(type_class.hdf5_type.class_, lib.H5T_STRING)
