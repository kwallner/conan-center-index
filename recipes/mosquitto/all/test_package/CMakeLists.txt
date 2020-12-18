cmake_minimum_required(VERSION 3.1)
project(test_package C)

file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/logo.png
     DESTINATION ${CMAKE_CURRENT_BINARY_DIR})

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

find_package(mosquitto REQUIRED)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} mosquittopp mosquitto)

