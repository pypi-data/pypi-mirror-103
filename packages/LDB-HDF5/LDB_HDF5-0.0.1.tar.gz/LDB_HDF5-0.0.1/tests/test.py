from __future__ import absolute_import

import unittest
import os

from ldb.hdf5._hdf5 import lib, ffi

import tests

def create_dataset(file_, dataset_name='dset'):
    dataset_name = dataset_name.encode('utf8')
    dims = ffi.new('hsize_t[2]', [10,10])
    dataspace = lib.H5Screate_simple(2, dims, ffi.NULL)
    dataset = lib.H5Dcreate2(file_, dataset_name, lib.H5T_STD_I32BE,
                             dataspace, lib.H5P_DEFAULT, lib.H5P_DEFAULT,
                             lib.H5P_DEFAULT)

    data = ffi.new('int[10][10]')
    for i, a in enumerate(data):
        for j, b in enumerate(a):
            a[j] = i*100 + j

    lib.H5Dwrite(dataset, lib.H5T_NATIVE_INT, lib.H5S_ALL, lib.H5S_ALL,
                 lib.H5P_DEFAULT, data)

    lib.H5Dclose(dataset)
    lib.H5Sclose(dataspace)


def create_attribute(file_, dataset_name='dset', attr_name='attr'):
    dataset_name = dataset_name.encode('utf8')
    attr_name = attr_name.encode('utf8')
    dataset = lib.H5Dopen2(file_, dataset_name, lib.H5P_DEFAULT)

    filetype = lib.H5Tcopy(lib.H5T_FORTRAN_S1)
    memtype = lib.H5Tcopy(lib.H5T_C_S1)
    lib.H5Tset_size(filetype, lib.H5T_VARIABLE)
    lib.H5Tset_size(memtype, lib.H5T_VARIABLE)

    dims = ffi.new('hsize_t[1]', [4])
    dataspace = lib.H5Screate_simple(1, dims, ffi.NULL)

    attr = lib.H5Acreate2(dataset, attr_name, filetype, dataspace,
                          lib.H5P_DEFAULT, lib.H5P_DEFAULT)

    strings = [ffi.new('char[]', b'Test'),
               ffi.new('char[]', b'me'),
               ffi.new('char[]', b''),
               ffi.new('char[]', b'much')]
    data = ffi.new('char*[]', strings)

    lib.H5Awrite(attr, memtype, data)

    lib.H5Aclose(attr)
    lib.H5Dclose(dataset)
    lib.H5Sclose(dataspace)


class BasicTestCase(tests.CleanupMixin, unittest.TestCase):
    def setUp(self):
        super(BasicTestCase, self).setUp()
        filename = os.path.join(self.save_dir, 'test_%s.h5'%(self.id()))
        self.file = lib.H5Fcreate(filename.encode("utf8"), lib.H5F_ACC_TRUNC,
                                  lib.H5P_DEFAULT, lib.H5P_DEFAULT)

    def tearDown(self):
        lib.H5Fclose(self.file)
        self.file = None
        super(BasicTestCase, self).tearDown()

    def testA(self):
        create_dataset(self.file)

        data = ffi.new('int[10][10]')
        dataset = lib.H5Dopen2(self.file, b'dset', lib.H5P_DEFAULT)
        lib.H5Dread(dataset, lib.H5T_NATIVE_INT, lib.H5S_ALL, lib.H5S_ALL,
                    lib.H5P_DEFAULT, data)

        for i, a in enumerate(data):
            for j, b in enumerate(a):
                self.assertEqual(b, i*100 + j)

    def testB(self):
        create_dataset(self.file)
        create_attribute(self.file)

        # TODO: Check attr is written
