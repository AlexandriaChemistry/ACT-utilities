#
# ACT-utilities: the Python modules and scripts of the Alexandria Chemistry
# Toolkit (ACT). ACT needs them, so install them before building ACT, into
# the same prefix or into the conda environment of ACT:
#
#   cmake -S . -B build -DCMAKE_INSTALL_PREFIX=<prefix of ACT>
#   cmake --install build
#
# The modules go to <prefix>/lib/pythonX.Y/site-packages/act_utilities, the
# scripts to <prefix>/bin and the data files to <prefix>/share/act. The file
# act_utilities.pth makes a Python with this site-packages find the modules,
# otherwise the file ACTRC of ACT adds them to PYTHONPATH. The directory
# site-packages/act, where the modules were until version 1.9b, is that of
# the Python package act of ACT; the installation removes the old files.
#
cmake_minimum_required(VERSION 3.24)

project(ACT-utilities VERSION 1.95 LANGUAGES NONE)

# The Python first in the PATH, for instance that of a conda environment,
# rather than the framework Python of macOS (Xcode), which CMake prefers
set(Python3_FIND_FRAMEWORK LAST)
find_package(Python3 REQUIRED COMPONENTS Interpreter)
if(NOT CMAKE_INSTALL_PYTHON_LIBDIR)
    set(CMAKE_INSTALL_PYTHON_LIBDIR
        "lib/python${Python3_VERSION_MAJOR}.${Python3_VERSION_MINOR}/site-packages")
endif()

include(CTest)

add_subdirectory(src)
add_subdirectory(share)
