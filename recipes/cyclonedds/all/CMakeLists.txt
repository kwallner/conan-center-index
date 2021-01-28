cmake_minimum_required(VERSION 3.5)
project(cyclonedds)

include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
conan_basic_setup()

include(CTest)

add_subdirectory(source_subfolder)

#install(
#  EXPORT CycloneDDS
#  NAMESPACE CycloneDDS::
#  FILE CycloneDDSTargets.cmake
#  DESTINATION .
#  )
#
#install(
#  FILES
#    ${CMAKE_CURRENT_BINARY_DIR}/CMakeFiles/Export/CycloneDDSTargets.cmake
#  DESTINATION
#    lib/CycloneDDS/cmake
#  )