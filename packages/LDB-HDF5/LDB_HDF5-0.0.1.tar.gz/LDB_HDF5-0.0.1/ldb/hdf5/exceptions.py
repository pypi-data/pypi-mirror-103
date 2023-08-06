# TODO: Check all return values for error (in low_level)

class HDF5Exception(Exception):
    pass

class DatasetExistsError(HDF5Exception):
    pass

class AttributeExistsError(HDF5Exception):
    pass
