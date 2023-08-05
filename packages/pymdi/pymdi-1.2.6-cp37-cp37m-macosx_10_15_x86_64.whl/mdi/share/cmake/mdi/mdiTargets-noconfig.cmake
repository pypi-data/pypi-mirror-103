#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "mdi::mdi" for configuration ""
set_property(TARGET mdi::mdi APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(mdi::mdi PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "/Users/tbarnes/Documents/mdi/MDI_Library/build/lib.macosx-10.9-x86_64-3.7/mdi/libmdi.1.dylib"
  IMPORTED_SONAME_NOCONFIG "@rpath/libmdi.1.dylib"
  )

list(APPEND _IMPORT_CHECK_TARGETS mdi::mdi )
list(APPEND _IMPORT_CHECK_FILES_FOR_mdi::mdi "/Users/tbarnes/Documents/mdi/MDI_Library/build/lib.macosx-10.9-x86_64-3.7/mdi/libmdi.1.dylib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
