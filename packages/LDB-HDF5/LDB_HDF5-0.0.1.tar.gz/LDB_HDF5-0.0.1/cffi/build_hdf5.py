from __future__ import absolute_import

import subprocess

from cffi import FFI

# TODO: Work out how to handle functions only available in certain versions

h5cc_pipe = subprocess.Popen(['h5cc', '-show'], stdout=subprocess.PIPE)
h5cc_result, _ = h5cc_pipe.communicate()
extra_args = h5cc_result.decode("utf8").split(" ")[1:]

ffi = FFI()

ffi.set_source("ldb.hdf5._hdf5",
               """
#include <hdf5.h>
               """,
               libraries=['hdf5'],
               extra_compile_args=extra_args,
               extra_link_args=extra_args,
              )

# Supported HDF APIs (aiming to be currently fully supporting):
# Unless otherwise stated:
# Assuming all functions have been declared
# This implies all types are at least sufficiently specified to declare funcs
# However, they my be shortcut specified (e.g. enums treated as blind ints)
# Constants are assumed incomplete unless otherwise specified
# Header complete means everything in the *public.h file should be in here
# H5A
# H5D
# H5F
# H5S
# H5T - header complete
ffi.cdef("""
typedef int... herr_t;
typedef int... hid_t;
typedef int... hssize_t;
typedef int... hbool_t;
typedef int... htri_t;
typedef int... haddr_t;

typedef int... ssize_t;
typedef int... hsize_t;


// Structs (or other types that opaque is fine for
typedef ... H5_index_t;
typedef ... H5_iter_order_t;

typedef ... H5A_info_t;

typedef ... H5AC_cache_config_t;

typedef ... H5D_space_status_t;

typedef ... H5F_mem_t;
//typedef ... H5F_sect_info_t;
typedef ... H5F_info_t;
//typedef ... H5F_retry_info_t;

typedef ... H5T_cdata_t;
typedef ... hvl_t;

typedef int... H5S_sel_type;
typedef int... H5S_seloper_t;


// TODO: Add all documented/useful constants
// constants
static const unsigned H5F_ACC_TRUNC;
static const unsigned H5F_ACC_EXCL;
static const unsigned H5F_ACC_RDWR;
static const unsigned H5F_ACC_RDONLY;
static const hid_t H5P_DEFAULT;
static const hid_t H5S_ALL;
static const hid_t H5S_SELECT_SET;


static const size_t H5T_VARIABLE;


// Enums
typedef enum H5F_scope_t {
    H5F_SCOPE_LOCAL,
    H5F_SCOPE_GLOBAL,
    ...
} H5F_scope_t;


typedef enum H5S_class_t {
    H5S_NO_CLASS,
    H5S_SCALAR,
    H5S_SIMPLE,
    H5S_NULL,
    ...
} H5S_class_t;


typedef enum H5T_bkg_t {
    H5T_BKG_NO,
    H5T_BKG_TEMP,
    H5T_BKG_YES,
    ...
} H5T_bkg_t;

typedef enum H5T_class_t {
    H5T_NO_CLASS,
    H5T_INTEGER,
    H5T_FLOAT,
    H5T_TIME,
    H5T_STRING,
    H5T_BITFIELD,
    H5T_OPAQUE,
    H5T_COMPOUND,
    H5T_REFERENCE,
    H5T_ENUM,
    H5T_VLEN,
    H5T_ARRAY,
    H5T_NCLASSES,
    ...
} H5T_class_t;

typedef enum H5T_cmd_t {
    H5T_CONV_INIT,
    H5T_CONV_CONV,
    H5T_CONV_FREE,
    ...
} H5T_cmd_t;

typedef enum H5T_conv_except_t {
    H5T_CONV_EXCEPT_RANGE_HI,
    H5T_CONV_EXCEPT_RANGE_LOW,
    H5T_CONV_EXCEPT_PRECISION,
    H5T_CONV_EXCEPT_TRUNCATE,
    H5T_CONV_EXCEPT_PINF,
    H5T_CONV_EXCEPT_NINF,
    H5T_CONV_EXCEPT_NAN,
    ...
} H5T_conv_except_t;

typedef enum H5T_conv_ret_t {
    H5T_CONV_ABORT,
    H5T_CONV_UNHANDLED,
    H5T_CONV_HANDLED,
    ...
} H5T_conv_ret_t;

typedef enum H5T_cset_t {
    H5T_CSET_ERROR,
    H5T_CSET_ASCII,
    H5T_CSET_UTF8,
    H5T_CSET_RESERVED_2,
    H5T_CSET_RESERVED_3,
    H5T_CSET_RESERVED_4,
    H5T_CSET_RESERVED_5,
    H5T_CSET_RESERVED_6,
    H5T_CSET_RESERVED_7,
    H5T_CSET_RESERVED_8,
    H5T_CSET_RESERVED_9,
    H5T_CSET_RESERVED_10,
    H5T_CSET_RESERVED_11,
    H5T_CSET_RESERVED_12,
    H5T_CSET_RESERVED_13,
    H5T_CSET_RESERVED_14,
    H5T_CSET_RESERVED_15,
    ...
} H5T_cset_t;

typedef enum H5T_direction_t {
    H5T_DIR_DEFAULT,
    H5T_DIR_ASCEND,
    H5T_DIR_DESCEND,
    ...
} H5T_direction_t;

typedef enum H5T_norm_t {
    H5T_NORM_ERROR,
    H5T_NORM_IMPLIED,
    H5T_NORM_MSBSET,
    H5T_NORM_NONE,
    ...
} H5T_norm_t;

typedef enum H5T_order_t {
    H5T_ORDER_ERROR,
    H5T_ORDER_LE,
    H5T_ORDER_BE,
    H5T_ORDER_VAX,
    H5T_ORDER_MIXED,
    H5T_ORDER_NONE,
    ...
} H5T_order_t;

typedef enum H5T_pad_t {
    H5T_PAD_ERROR,
    H5T_PAD_ZERO,
    H5T_PAD_ONE,
    H5T_PAD_BACKGROUND,
    H5T_NPAD,
    ...
} H5T_pad_t;

typedef enum H5T_pers_t {
    H5T_PERS_DONTCARE,
    H5T_PERS_HARD,
    H5T_PERS_SOFT,
    ...
} H5T_pers_t;

typedef enum H5T_sign_t {
    H5T_SGN_ERROR,
    H5T_SGN_NONE,
    H5T_SGN_2,
    H5T_NSGN,
    ...
} H5T_sign_t;

typedef enum H5T_str_t {
    H5T_STR_ERROR,
    H5T_STR_NULLTERM,
    H5T_STR_NULLPAD,
    H5T_STR_SPACEPAD,
    H5T_STR_RESERVED_3,
    H5T_STR_RESERVED_4,
    H5T_STR_RESERVED_5,
    H5T_STR_RESERVED_6,
    H5T_STR_RESERVED_7,
    H5T_STR_RESERVED_8,
    H5T_STR_RESERVED_9,
    H5T_STR_RESERVED_10,
    H5T_STR_RESERVED_11,
    H5T_STR_RESERVED_12,
    H5T_STR_RESERVED_13,
    H5T_STR_RESERVED_14,
    H5T_STR_RESERVED_15,
    ...
} H5T_str_t;






// H5T type constants
static const hid_t H5T_IEEE_F32BE;
static const hid_t H5T_IEEE_F32LE;
static const hid_t H5T_IEEE_F64BE;
static const hid_t H5T_IEEE_F64LE;

static const hid_t H5T_STD_I8BE;
static const hid_t H5T_STD_I8LE;
static const hid_t H5T_STD_I16BE;
static const hid_t H5T_STD_I16LE;
static const hid_t H5T_STD_I32BE;
static const hid_t H5T_STD_I32LE;
static const hid_t H5T_STD_I64BE;
static const hid_t H5T_STD_I64LE;
static const hid_t H5T_STD_U8BE;
static const hid_t H5T_STD_U8LE;
static const hid_t H5T_STD_U16BE;
static const hid_t H5T_STD_U16LE;
static const hid_t H5T_STD_U32BE;
static const hid_t H5T_STD_U32LE;
static const hid_t H5T_STD_U64BE;
static const hid_t H5T_STD_U64LE;
static const hid_t H5T_STD_B8BE;
static const hid_t H5T_STD_B8LE;
static const hid_t H5T_STD_B16BE;
static const hid_t H5T_STD_B16LE;
static const hid_t H5T_STD_B32BE;
static const hid_t H5T_STD_B32LE;
static const hid_t H5T_STD_B64BE;
static const hid_t H5T_STD_B64LE;

static const hid_t H5T_STD_REF_OBJ;
static const hid_t H5T_STD_REF_DSETREG;

static const hid_t H5T_UNIX_D32BE;
static const hid_t H5T_UNIX_D32LE;
static const hid_t H5T_UNIX_D64BE;
static const hid_t H5T_UNIX_D64LE;

static const hid_t H5T_C_S1;
static const hid_t H5T_FORTRAN_S1;

static const hid_t H5T_INTEL_I8;
static const hid_t H5T_INTEL_I16;
static const hid_t H5T_INTEL_I32;
static const hid_t H5T_INTEL_I64;
static const hid_t H5T_INTEL_U8;
static const hid_t H5T_INTEL_U16;
static const hid_t H5T_INTEL_U32;
static const hid_t H5T_INTEL_U64;
static const hid_t H5T_INTEL_B8;
static const hid_t H5T_INTEL_B16;
static const hid_t H5T_INTEL_B32;
static const hid_t H5T_INTEL_B64;
static const hid_t H5T_INTEL_F32;
static const hid_t H5T_INTEL_F64;

static const hid_t H5T_ALPHA_I8;
static const hid_t H5T_ALPHA_I16;
static const hid_t H5T_ALPHA_I32;
static const hid_t H5T_ALPHA_I64;
static const hid_t H5T_ALPHA_U8;
static const hid_t H5T_ALPHA_U16;
static const hid_t H5T_ALPHA_U32;
static const hid_t H5T_ALPHA_U64;
static const hid_t H5T_ALPHA_B8;
static const hid_t H5T_ALPHA_B16;
static const hid_t H5T_ALPHA_B32;
static const hid_t H5T_ALPHA_B64;
static const hid_t H5T_ALPHA_F32;
static const hid_t H5T_ALPHA_F64;

static const hid_t H5T_MIPS_I8;
static const hid_t H5T_MIPS_I16;
static const hid_t H5T_MIPS_I32;
static const hid_t H5T_MIPS_I64;
static const hid_t H5T_MIPS_U8;
static const hid_t H5T_MIPS_U16;
static const hid_t H5T_MIPS_U32;
static const hid_t H5T_MIPS_U64;
static const hid_t H5T_MIPS_B8;
static const hid_t H5T_MIPS_B16;
static const hid_t H5T_MIPS_B32;
static const hid_t H5T_MIPS_B64;
static const hid_t H5T_MIPS_F32;
static const hid_t H5T_MIPS_F64;

static const hid_t H5T_VAX_F32;
static const hid_t H5T_VAX_F64;

static const hid_t H5T_NATIVE_CHAR;
static const hid_t H5T_NATIVE_SCHAR;
static const hid_t H5T_NATIVE_UCHAR;
static const hid_t H5T_NATIVE_SHORT;
static const hid_t H5T_NATIVE_USHORT;
static const hid_t H5T_NATIVE_INT;
static const hid_t H5T_NATIVE_UINT;
static const hid_t H5T_NATIVE_LONG;
static const hid_t H5T_NATIVE_ULONG;
static const hid_t H5T_NATIVE_LLONG;
static const hid_t H5T_NATIVE_ULLONG;
static const hid_t H5T_NATIVE_FLOAT;
static const hid_t H5T_NATIVE_DOUBLE;
static const hid_t H5T_NATIVE_LDOUBLE;
static const hid_t H5T_NATIVE_B8;
static const hid_t H5T_NATIVE_B16;
static const hid_t H5T_NATIVE_B32;
static const hid_t H5T_NATIVE_B64;
static const hid_t H5T_NATIVE_OPAQUE;
static const hid_t H5T_NATIVE_HADDR;
static const hid_t H5T_NATIVE_HSIZE;
static const hid_t H5T_NATIVE_HSSIZE;
static const hid_t H5T_NATIVE_HERR;
static const hid_t H5T_NATIVE_HBOOL;

static const hid_t H5T_NATIVE_INT8;
static const hid_t H5T_NATIVE_UINT8;
static const hid_t H5T_NATIVE_INT_LEAST8;
static const hid_t H5T_NATIVE_UINT_LEAST8;
static const hid_t H5T_NATIVE_INT_FAST8;
static const hid_t H5T_NATIVE_UINT_FAST8;
static const hid_t H5T_NATIVE_INT16;
static const hid_t H5T_NATIVE_UINT16;
static const hid_t H5T_NATIVE_INT_LEAST16;
static const hid_t H5T_NATIVE_UINT_LEAST16;
static const hid_t H5T_NATIVE_INT_FAST16;
static const hid_t H5T_NATIVE_UINT_FAST16;
static const hid_t H5T_NATIVE_INT32;
static const hid_t H5T_NATIVE_UINT32;
static const hid_t H5T_NATIVE_INT_LEAST32;
static const hid_t H5T_NATIVE_UINT_LEAST32;
static const hid_t H5T_NATIVE_INT_FAST32;
static const hid_t H5T_NATIVE_UINT_FAST32;
static const hid_t H5T_NATIVE_INT64;
static const hid_t H5T_NATIVE_UINT64;
static const hid_t H5T_NATIVE_INT_LEAST64;
static const hid_t H5T_NATIVE_UINT_LEAST64;
static const hid_t H5T_NATIVE_INT_FAST64;
static const hid_t H5T_NATIVE_UINT_FAST64;


// Function pointer types
typedef herr_t (*H5A_operator2_t)( hid_t location_id, const char *attr_name,
                                   const H5A_info_t *ainfo, void *op_data);

typedef herr_t (*H5D_gather_func_t)( const void * dst_buf,
                                     size_t dst_buf_bytes_used, void *op_data);
typedef herr_t (*H5D_operator_t)(void* elem, hid_t type_id, unsigned ndim, 
                                 const hsize_t *point, void *operator_data);
typedef herr_t (*H5D_scatter_func_t)( const void ** src_buf/*out*/,
                                      size_t *src_buf_bytes_used/*out*/,
                                      void *op_data);

typedef herr_t (*H5T_conv_t) (hid_t src_id, hid_t dst_id, H5T_cdata_t *cdata,
                              size_t nelmts, size_t buf_stride,
                              size_t bkg_stride, void *buf, void *bkg,
                              hid_t dset_xfer_plist);
typedef H5T_conv_ret_t (*H5T_conv_except_func_t)(H5T_conv_except_t except_type,
                                                 hid_t src_id, hid_t dst_id,
                                                 void *src_buf, void *dst_buf,
                                                 void *user_data);


// Function declarations

// H5A
herr_t H5Aclose(hid_t attr_id);
hid_t H5Acreate2( hid_t loc_id, const char *attr_name, hid_t type_id,
                  hid_t space_id, hid_t acpl_id, hid_t aapl_id );
hid_t H5Acreate_by_name( hid_t loc_id, const char *obj_name,
                         const char *attr_name, hid_t type_id, hid_t space_id,
                         hid_t acpl_id, hid_t aapl_id, hid_t lapl_id );
herr_t H5Adelete( hid_t loc_id, const char *attr_name );
herr_t H5Adelete_by_name( hid_t loc_id, const char *obj_name,
                          const char *attr_name, hid_t lapl_id );
herr_t H5Adelete_by_idx( hid_t loc_id, const char *obj_name,
                         H5_index_t idx_type, H5_iter_order_t order, hsize_t n,
                         hid_t lapl_id );
htri_t H5Aexists( hid_t obj_id, const char *attr_name );
htri_t H5Aexists_by_name( hid_t loc_id, const char *obj_name,
                          const char *attr_name, hid_t lapl_id );
hid_t H5Aget_create_plist(hid_t attr_id);
herr_t H5Aget_info( hid_t attr_id, H5A_info_t *ainfo );
herr_t H5Aget_info_by_idx( hid_t loc_id, const char *obj_name,
                           H5_index_t idx_type, H5_iter_order_t order,
                           hsize_t n, H5A_info_t *ainfo, hid_t lapl_id );
herr_t H5Aget_info_by_name( hid_t loc_id, const char *obj_name,
                            const char *attr_name, H5A_info_t *ainfo,
                            hid_t lapl_id );
ssize_t H5Aget_name(hid_t attr_id, size_t buf_size, char *buf );
ssize_t H5Aget_name_by_idx( hid_t loc_id, const char *obj_name,
                            H5_index_t idx_type, H5_iter_order_t order,
                            hsize_t n, char *name, size_t size,
                            hid_t lapl_id );
int H5Aget_num_attrs( hid_t loc_id );
hid_t H5Aget_space(hid_t attr_id);
hsize_t H5Aget_storage_size(hid_t attr_id);
hid_t H5Aget_type(hid_t attr_id);
herr_t H5Aiterate2( hid_t obj_id, H5_index_t idx_type, H5_iter_order_t order,
                    hsize_t *n, H5A_operator2_t op, void *op_data );
herr_t H5Aiterate_by_name( hid_t loc_id, const char *obj_name,
                           H5_index_t idx_type, H5_iter_order_t order,
                           hsize_t *n, H5A_operator2_t op, void *op_data,
                           hid_t lapd_id );
hid_t H5Aopen( hid_t obj_id, const char *attr_name, hid_t aapl_id );
hid_t H5Aopen_by_idx( hid_t loc_id, const char *obj_name, H5_index_t idx_type,
                      H5_iter_order_t order, hsize_t n, hid_t aapl_id,
                      hid_t lapl_id );
hid_t H5Aopen_by_name( hid_t loc_id, const char *obj_name,
                       const char *attr_name, hid_t aapl_id, hid_t lapl_id );
hid_t H5Aopen_idx( hid_t loc_id, unsigned int idx );
hid_t H5Aopen_name( hid_t loc_id, const char *name );
herr_t H5Aread(hid_t attr_id, hid_t mem_type_id, void *buf );
herr_t H5Arename( hid_t loc_id, char *old_attr_name, char *new_attr_name );
herr_t H5Arename_by_name( hid_t loc_id, const char *obj_name,
                          const char *old_attr_name, const char *new_attr_name,
                          hid_t lapl_id );
herr_t H5Awrite(hid_t attr_id, hid_t mem_type_id, const void *buf );


// H5D
herr_t H5Dclose(hid_t dataset_id );
hid_t H5Dcreate2( hid_t loc_id, const char *name, hid_t dtype_id,
                  hid_t space_id, hid_t lcpl_id, hid_t dcpl_id,
                  hid_t dapl_id );
hid_t H5Dcreate_anon( hid_t loc_id, hid_t type_id, hid_t space_id,
                      hid_t dcpl_id, hid_t dapl_id );
herr_t H5Dextend( hid_t dataset_id, const hsize_t size[] );
herr_t H5Dfill( const void *fill, hid_t fill_type_id, void *buf,
                hid_t buf_type_id, hid_t space_id );
//herr_t H5Dflush(hid_t dataset_id);
herr_t H5Dgather( hid_t src_space_id, const void * src_buf, hid_t type_id,
                  size_t dst_buf_size, void *dst_buf, H5D_gather_func_t op,
                  void * op_data );
hid_t H5Dget_access_plist( hid_t dataset_id );
hid_t H5Dget_create_plist(hid_t dataset_id );
haddr_t H5Dget_offset( hid_t dset_id );
hid_t H5Dget_space( hid_t dataset_id );
herr_t H5Dget_space_status(hid_t dset_id, H5D_space_status_t *status);
hsize_t H5Dget_storage_size( hid_t dataset_id );
hid_t H5Dget_type(hid_t dataset_id );
herr_t H5Diterate( void *buf, hid_t type_id, hid_t space_id,
                   H5D_operator_t operator, void *operator_data );
hid_t H5Dopen2( hid_t loc_id, const char *name, hid_t dapl_id );
herr_t H5Dread( hid_t dataset_id, hid_t mem_type_id, hid_t mem_space_id,
                hid_t file_space_id, hid_t xfer_plist_id, void * buf );
//herr_t H5Drefresh(hid_t dataset_id);
herr_t H5Dscatter( H5D_scatter_func_t op, void * op_data, hid_t type_id,
                   hid_t dst_space_id, void *dst_buf );
herr_t H5Dset_extent( hid_t dset_id, const hsize_t size[] );
herr_t H5Dvlen_get_buf_size(hid_t dataset_id, hid_t type_id, hid_t space_id,
                            hsize_t *size );
herr_t H5Dvlen_reclaim( hid_t type_id, hid_t space_id, hid_t plist_id,
                        void *buf );
herr_t H5Dwrite( hid_t dataset_id, hid_t mem_type_id, hid_t mem_space_id,
                 hid_t file_space_id, hid_t xfer_plist_id, const void * buf );


// H5F
herr_t H5Fclear_elink_file_cache( hid_t file_id );
herr_t H5Fclose( hid_t file_id );
hid_t H5Fcreate( const char *name, unsigned flags, hid_t fcpl_id,
                 hid_t fapl_id );
herr_t H5Fflush(hid_t object_id, H5F_scope_t scope );
hid_t H5Fget_access_plist(hid_t file_id);
hid_t H5Fget_create_plist(hid_t file_id );
ssize_t H5Fget_file_image( hid_t file_id, void *buf_ptr, size_t buf_len );
herr_t H5Fget_filesize( hid_t file_id, hsize_t *size );
//ssize_t H5Fget_free_sections( hid_t fcpl_id, H5F_mem_t type, size_t nsects,
//                              H5F_sect_info_t * sect_info );
hssize_t H5Fget_freespace( hid_t file_id );
herr_t H5Fget_info( hid_t obj_id, H5F_info_t *file_info );
herr_t H5Fget_intent( hid_t file_id, unsigned *intent );
herr_t H5Fget_mdc_config(hid_t file_id, H5AC_cache_config_t *config_ptr);
herr_t H5Fget_mdc_hit_rate(hid_t file_id, double *hit_rate_ptr);
//herr_t H5Fget_mdc_logging_status( hid_t file_id, hbool_t *is_enabled,
//                                  hbool_t *is_currently_logging );
herr_t H5Fget_mdc_size(hid_t file_id, size_t *max_size_ptr,
                       size_t *min_clean_size_ptr, size_t *cur_size_ptr,
                       int *cur_num_entries_ptr);
//herr_t H5Fget_metadata_read_retry_info( hid_t file_id,
//                                        H5F_retry_info_t *info );
//herr_t H5Fget_mpi_atomicity( hid_t file_id, hbool_t *flag );
ssize_t H5Fget_name(hid_t obj_id, char *name, size_t size );
ssize_t H5Fget_obj_count( hid_t file_id, unsigned int types );
ssize_t H5Fget_obj_ids( hid_t file_id, unsigned int types, size_t max_objs,
                        hid_t *obj_id_list );
herr_t H5Fget_vfd_handle(hid_t file_id, hid_t fapl_id, void **file_handle );
htri_t H5Fis_hdf5(const char *name );
herr_t H5Fmount(hid_t loc_id, const char *name, hid_t child_id,
                hid_t fmpl_id );
hid_t H5Fopen( const char *name, unsigned flags, hid_t fapl_id );
hid_t H5Freopen(hid_t file_id );
herr_t H5Freset_mdc_hit_rate_stats(hid_t file_id);
herr_t H5Fset_mdc_config(hid_t file_id, H5AC_cache_config_t *config_ptr);
//herr_t H5Fset_mpi_atomicity( hid_t file_id, hbool_t flag );
//herr_t H5Fstart_swmr_write(hid_t file_id);
//herr_t H5Fstart_mdc_logging( hid_t file_id );
//herr_t H5Fstop_mdc_logging( hid_t file_id );
herr_t H5Funmount(hid_t loc_id, const char *name );


// H5S
herr_t H5Sclose( hid_t space_id );
hid_t H5Scopy( hid_t space_id );
hid_t H5Screate( H5S_class_t type );
hid_t H5Screate_simple( int rank, const hsize_t * current_dims,
                        const hsize_t * maximum_dims );
hid_t H5Sdecode (unsigned char *buf);
herr_t H5Sencode(hid_t obj_id, unsigned char *buf, size_t *nalloc);
herr_t H5Sextent_copy(hid_t dest_space_id, hid_t source_space_id );
htri_t H5Sextent_equal( hid_t space1_id, hid_t space2_id );
//herr_t H5Sget_regular_hyperslab( hid_t space_id, hsize_t start[],
//                                 hsize_t stride[], hsize_t count[],
//                                 hsize_t block[] );
herr_t H5Sget_select_bounds(hid_t space_id, hsize_t *start, hsize_t *end );
hssize_t H5Sget_select_elem_npoints(hid_t space_id );
herr_t H5Sget_select_elem_pointlist(hid_t space_id, hsize_t startpoint,
                                    hsize_t numpoints, hsize_t *buf );
herr_t H5Sget_select_hyper_blocklist(hid_t space_id, hsize_t startblock,
                                     hsize_t numblocks, hsize_t *buf );
hssize_t H5Sget_select_hyper_nblocks( hid_t space_id );
hssize_t H5Sget_select_npoints( hid_t space_id );
H5S_sel_type H5Sget_select_type(hid_t space_id);
int H5Sget_simple_extent_dims(hid_t space_id, hsize_t *dims,
                              hsize_t *maxdims );
int H5Sget_simple_extent_ndims( hid_t space_id );
hssize_t H5Sget_simple_extent_npoints( hid_t space_id );
H5S_class_t H5Sget_simple_extent_type( hid_t space_id );
//htri_t H5Sis_regular_hyperslab( hid_t space_id );
htri_t H5Sis_simple( hid_t space_id );
herr_t H5Soffset_simple(hid_t space_id, const hssize_t *offset );
herr_t H5Sselect_all( hid_t dspace_id );
herr_t H5Sselect_elements( hid_t space_id, H5S_seloper_t op,
                           size_t num_elements, const hsize_t *coord );
herr_t H5Sselect_hyperslab(hid_t space_id, H5S_seloper_t op,
                           const hsize_t *start, const hsize_t *stride,
                           const hsize_t *count, const hsize_t *block );
herr_t H5Sselect_none(hid_t space_id);
htri_t H5Sselect_valid( hid_t space_id );
herr_t H5Sset_extent_none( hid_t space_id );
herr_t H5Sset_extent_simple( hid_t space_id, int rank,
                             const hsize_t *current_size,
                             const hsize_t *maximum_size );


// H5T
// TODO: Add the rest
hid_t H5Tarray_create2( hid_t base_type_id, unsigned rank,
                        const hsize_t dims[] );
herr_t H5Tclose( hid_t dtype_id );
herr_t H5Tcommit2( hid_t loc_id, const char *name, hid_t dtype_id,
                   hid_t lcpl_id, hid_t tcpl_id, hid_t tapl_id );
herr_t H5Tcommit_anon( hid_t loc_id, hid_t dtype_id, hid_t tcpl_id,
                       hid_t tapl_id );
htri_t H5Tcommitted( hid_t dtype_id );
htri_t H5Tcompiler_conv(hid_t src_id, hid_t dst_id);
herr_t H5Tconvert( hid_t src_type_id, hid_t dest_type_id, size_t nelmts,
                   void *buf, void *background, hid_t plist_id );
hid_t H5Tcopy( hid_t dtype_id );
hid_t H5Tcreate( H5T_class_t class, size_t size );
hid_t H5Tdecode (unsigned char *buf);
htri_t H5Tdetect_class( hid_t dtype_id, H5T_class_t dtype_class );
herr_t H5Tencode(hid_t obj_id, unsigned char *buf, size_t *nalloc);
hid_t H5Tenum_create( hid_t dtype_id );
herr_t H5Tenum_insert( hid_t dtype_id, const char *name, void *value );
herr_t H5Tenum_nameof( hid_t dtype_id, void *value, char *name, size_t size );
herr_t H5Tenum_valueof( hid_t dtype_id, char *name, void *value );
htri_t H5Tequal( hid_t dtype_id1, hid_t dtype_id2 );
H5T_conv_t H5Tfind(hid_t src_id, hid_t dst_id, H5T_cdata_t **pcdata );
//herr_t H5Tflush(hid_t dtype_id);
int H5Tget_array_dims2( hid_t adtype_id, hsize_t dims[] );
int H5Tget_array_ndims( hid_t adtype_id );
H5T_class_t H5Tget_class( hid_t dtype_id );
hid_t H5Tget_create_plist( hid_t dtype_id );
H5T_cset_t H5Tget_cset( hid_t dtype_id );
size_t H5Tget_ebias( hid_t dtype_id );
herr_t H5Tget_fields( hid_t dtype_id, size_t *spos, size_t *epos,
                      size_t *esize, size_t *mpos, size_t *msize );
H5T_pad_t H5Tget_inpad( hid_t dtype_id );
H5T_class_t H5Tget_member_class( hid_t cdtype_id, unsigned member_no );
int H5Tget_member_index( hid_t dtype_id, const char * field_name );
char * H5Tget_member_name( hid_t dtype_id, unsigned field_idx );
size_t H5Tget_member_offset( hid_t dtype_id, unsigned memb_no );
hid_t H5Tget_member_type( hid_t dtype_id, unsigned field_idx );
herr_t H5Tget_member_value( hid_t dtype_id, unsigned memb_no, void *value );
hid_t H5Tget_native_type( hid_t dtype_id, H5T_direction_t direction );
int H5Tget_nmembers( hid_t dtype_id );
H5T_norm_t H5Tget_norm( hid_t dtype_id );
int H5Tget_offset( hid_t dtype_id );
H5T_order_t H5Tget_order( hid_t dtype_id );
herr_t H5Tget_pad( hid_t dtype_id, H5T_pad_t * lsb, H5T_pad_t * msb );
size_t H5Tget_precision( hid_t dtype_id );
H5T_sign_t H5Tget_sign( hid_t dtype_id );
size_t H5Tget_size( hid_t dtype_id );
H5T_str_t H5Tget_strpad( hid_t dtype_id );
hid_t H5Tget_super( hid_t dtype_id );
char *H5Tget_tag( hid_t dtype_id );
herr_t H5Tinsert( hid_t dtype_id, const char * name, size_t offset,
                  hid_t field_id );
htri_t H5Tis_variable_str( hid_t dtype_id );
herr_t H5Tlock( hid_t dtype_id );
hid_t H5Topen2( hid_t loc_id, const char * name, hid_t tapl_id );
herr_t H5Tpack( hid_t dtype_id );
//herr_t H5Trefresh(hid_t dtype_id);
herr_t H5Tregister( H5T_pers_t type, const char * name, hid_t src_id,
                    hid_t dst_id, H5T_conv_t func );
herr_t H5Tset_cset( hid_t dtype_id, H5T_cset_t cset );
herr_t H5Tset_ebias( hid_t dtype_id, size_t ebias );
herr_t H5Tset_fields( hid_t dtype_id, size_t spos, size_t epos, size_t esize,
                      size_t mpos, size_t msize );
herr_t H5Tset_inpad( hid_t dtype_id, H5T_pad_t inpad );
herr_t H5Tset_norm( hid_t dtype_id, H5T_norm_t norm );
herr_t H5Tset_offset( hid_t dtype_id, size_t offset );
herr_t H5Tset_order( hid_t dtype_id, H5T_order_t order );
herr_t H5Tset_pad( hid_t dtype_id, H5T_pad_t lsb, H5T_pad_t msb );
herr_t H5Tset_precision( hid_t dtype_id, size_t precision );
herr_t H5Tset_sign( hid_t dtype_id, H5T_sign_t sign );
herr_t H5Tset_size( hid_t dtype_id, size_t size );
herr_t H5Tset_strpad( hid_t dtype_id, H5T_str_t strpad );
herr_t H5Tset_tag( hid_t dtype_id, const char *tag );
herr_t H5Tunregister( H5T_pers_t type, const char *name, hid_t src_id,
                      hid_t dst_id, H5T_conv_t func );
hid_t H5Tvlen_create( hid_t base_type_id );
         """)
