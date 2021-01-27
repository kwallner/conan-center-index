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

add_subdirectory(source_subfolder)

if (BUILD_GMOCK)
  if (GTEST_NO_MAIN)
    install(TARGETS gtest gmock EXPORT GTest)
  else()
    install(TARGETS gtest gtest_main gmock gmock_main EXPORT GTest)
  endif()
else()
  if (GTEST_NO_MAIN)
    install(TARGETS gtest EXPORT GTest)
  else()
    install(TARGETS gtest gtest_main EXPORT GTest)
  endif()
endif()

install(
  EXPORT GTest
  NAMESPACE GTest::
  FILE GTestTargets.cmake
  DESTINATION share/GTest/cmake
  )

install(
  FILES
    ${CMAKE_CURRENT_SOURCE_DIR}/source_subfolder/googletest/generated/GTestConfigVersion.cmake
    ${CMAKE_CURRENT_SOURCE_DIR}/source_subfolder/googletest/generated/GTestConfig.cmake
    ${CMAKE_CURRENT_BINARY_DIR}/CMakeFiles/Export/share/GTest/cmake/GTestTargets.cmake
  DESTINATION
  share/GTest/cmake
  )

