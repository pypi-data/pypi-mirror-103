import sys

from setuptools import setup

if "--keep-files" in sys.argv:
    import tests
    tests.keep_test_output_files = True
    sys.argv.remove("--keep-files")

setup(name="LDB_HDF5",
      version="0.0.1",
      description="""
Wrapper module for HDF5. Written using cffi such that both CPython and pypy are
supported.""",
      author="Alex Orange",
      author_email="alex@eldebe.org",
      packages=['ldb', 'ldb.hdf5'],
      namespace_packages=['ldb'],
      url='http://www.eldebe.org/ldb/hdf5/',
      license='AGPLv3',
      classifiers=["Development Status :: 2 - Pre-Alpha",
                   "Intended Audience :: Developers",
                   "Intended Audience :: Information Technology",
                   "Intended Audience :: Science/Research",
                   "License :: OSI Approved :: GNU Affero General Public License v3",
                   "Programming Language :: Python",
                   "Programming Language :: Python :: Implementation :: CPython",
                   "Programming Language :: Python :: Implementation :: PyPy",
                   "Topic :: Database",
                   "Topic :: Scientific/Engineering",
                  ],
      setup_requires=['cffi>=1.0.0', 'setuptools_hg',
                      'LDB_Setuptools_Coverage'],
      cffi_modules=['cffi/build_hdf5.py:ffi'],
      install_requires=['cffi>=1.0.0'],
      test_suite='tests',
      tests_requires=['cffi>=1.0.0'],
     )
