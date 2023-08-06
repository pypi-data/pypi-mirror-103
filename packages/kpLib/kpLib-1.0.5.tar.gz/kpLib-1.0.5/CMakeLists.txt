cmake_minimum_required(VERSION 2.6)

project(kplib)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -Wall -Werror -fPIC")
set(CMAKE_CXX_FLAGS_DEBUG "-O0 -g")                 # Debug mode.
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -march=native")    # Default optimization.
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif(NOT CMAKE_BUILD_TYPE)

#set(CMAKE_VERBOSE_MAKEFILE ON)  # use make VERBOSE=1 instead of set verbose as default

include_directories(${PROJECT_SOURCE_DIR}/include)
set(SOURCES ${PROJECT_SOURCE_DIR}/src/msmath.cpp
            ${PROJECT_SOURCE_DIR}/src/kPointLattice.cpp
            ${PROJECT_SOURCE_DIR}/src/kPointLatticeGenerator.cpp)

# static library
add_library(kplib_static STATIC ${SOURCES})
set_property(TARGET kplib_static PROPERTY OUTPUT_NAME kpoints)

# shared library
add_library(kplib_shared SHARED ${SOURCES})
set_property(TARGET kplib_shared PROPERTY OUTPUT_NAME kpoints)

# demo_kplib
#add_subdirectory(./demo_kplib ./demo_kplib/build)
