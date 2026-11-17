#
# ACT-utilities: the Python modules and scripts of the Alexandria Chemistry
# Toolkit (ACT). ACT needs them, so install them before building ACT, into
# the same prefix or into the conda environment of ACT:
#
#   cmake -S . -B build -DCMAKE_INSTALL_PREFIX=<prefix of ACT>
#   cmake --install build
#
# The modules go to <prefix>/lib/pythonX.Y/site-packages/act, the scripts to
# <prefix>/bin. The file act.pth makes a Python with this site-packages find
# the modules, otherwise the file ACTRC of ACT adds them to PYTHONPATH.
#
cmake_minimum_required(VERSION 3.24)

project(ACT-utilities VERSION 1.9 LANGUAGES NONE)

find_package(Python3 REQUIRED COMPONENTS Interpreter)
if(NOT CMAKE_INSTALL_PYTHON_LIBDIR)
    set(CMAKE_INSTALL_PYTHON_LIBDIR
        "lib/python${Python3_VERSION_MAJOR}.${Python3_VERSION_MINOR}/site-packages")
endif()

include(CTest)

add_subdirectory(src)
