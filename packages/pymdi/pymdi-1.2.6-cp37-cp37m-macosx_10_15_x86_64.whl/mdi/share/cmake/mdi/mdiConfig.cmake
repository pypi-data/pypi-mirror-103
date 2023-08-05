# mdiConfig.cmake
# --------------------
#
# MDI_Library cmake module.
# This module sets the following variables in your project::
#
#   mdi_FOUND - true if MDI_Library and all required components found on the system
#   mdi_VERSION - MDI_Library version in format Major.Minor.Release
#   mdi_INCLUDE_DIRS - Directory where MDI_Library header is located.
#   mdi_INCLUDE_DIR - same as DIRS
#   mdi_LIBRARIES - MDI_Library library to link against.
#   mdi_LIBRARY - same as LIBRARIES
#
#
# Exported targets::
#
# If the MDI_Library is found, this module defines the following :prop_tgt:`IMPORTED`
# target. Target is shared _or_ static, so, for both, use separate, not
# overlapping, installations. ::
#
#   mdi::mdi - the main MDI library with header attached.
#
#
# Suggested usage::
#
#   find_package(mdi)
#   find_package(mdi 1.0.1 EXACT CONFIG REQUIRED)


####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was mdiConfig.cmake.in                            ########

get_filename_component(PACKAGE_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../" ABSOLUTE)

macro(set_and_check _var _file)
  set(${_var} "${_file}")
  if(NOT EXISTS "${_file}")
    message(FATAL_ERROR "File or directory ${_file} referenced by variable ${_var} does not exist !")
  endif()
endmacro()

macro(check_required_components _NAME)
  foreach(comp ${${_NAME}_FIND_COMPONENTS})
    if(NOT ${_NAME}_${comp}_FOUND)
      if(${_NAME}_FIND_REQUIRED_${comp})
        set(${_NAME}_FOUND FALSE)
      endif()
    endif()
  endforeach()
endmacro()

####################################################################################

set(PN mdi)

if()
    set(${PN}_shared_FOUND 1)
else()
    set(${PN}_static_FOUND 1)
endif()

check_required_components(${PN})

#-----------------------------------------------------------------------------
# Don't include targets if this file is being picked up by another
# project which has already built this as a subproject
#-----------------------------------------------------------------------------
if(NOT TARGET ${PN}::mdi)
    include("${CMAKE_CURRENT_LIST_DIR}/${PN}Targets.cmake")

    get_property(_loc TARGET ${PN}::mdi PROPERTY LOCATION)
    set(${PN}_LIBRARY ${_loc})
    get_property(_ill TARGET ${PN}::mdi PROPERTY INTERFACE_LINK_LIBRARIES)
    set(${PN}_LIBRARIES ${_ill})

    get_property(_id TARGET ${PN}::mdi PROPERTY INCLUDE_DIRECTORIES)
    set(${PN}_INCLUDE_DIR ${_id})
    get_property(_iid TARGET ${PN}::mdi PROPERTY INTERFACE_INCLUDE_DIRECTORIES)
    set(${PN}_INCLUDE_DIRS ${_iid})
endif()
