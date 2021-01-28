cmake_minimum_required(VERSION 3.5)
project(iceoryx)

include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
conan_basic_setup()

include(CTest)

add_subdirectory(source_subfolder/iceoryx_meta)
