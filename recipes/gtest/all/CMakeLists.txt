cmake_minimum_required(VERSION 2.8.11)
project(cmake_wrapper)

include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
conan_basic_setup()

option(GTEST_NO_MAIN "Generate google main libraries" OFF)

if(MSVC)
  if(MSVC_VERSION AND MSVC_VERSION GREATER_EQUAL 1910)
    add_definitions(-DGTEST_LANG_CXX11=1 -DGTEST_HAS_TR1_TUPLE=0)
  endif(MSVC_VERSION AND MSVC_VERSION GREATER_EQUAL 1910)
endif(MSVC)

add_subdirectory("source_subfolder")

include(CMakePackageConfigHelpers)
write_basic_package_version_file(
  ${CMAKE_CURRENT_BINARY_DIR}/GTestConfigVersion.cmake
  VERSION ${GTEST_VERSION}
  COMPATIBILITY SameMajorVersion)
configure_file(cmake/GTestConfig.cmake.in
               ${CMAKE_CURRENT_BINARY_DIR}/GTestConfig.cmake
               COPYONLY)

if (BUILD_GMOCK)
  export(TARGETS gtest gtest_main gmock gmock_main
        FILE ${CMAKE_CURRENT_BINARY_DIR}/GTestTargets.cmake
       )
else()
  export(TARGETS gtest gtest_main
       FILE ${CMAKE_CURRENT_BINARY_DIR}/GTestTargets.cmake
      )
endif()
install(FILES
          ${CMAKE_CURRENT_BINARY_DIR}/GTestConfigVersion.cmake
          ${CMAKE_CURRENT_BINARY_DIR}/GTestTargets.cmake
          ${CMAKE_CURRENT_BINARY_DIR}/GTestConfig.cmake
        DESTINATION
          .)

