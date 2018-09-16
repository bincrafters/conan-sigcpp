cmake_minimum_required(VERSION 2.8.12)
project(PackageTest CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(test_bind test_bind.cc testutilities.cc)
target_link_libraries(test_bind ${CONAN_LIBS})
