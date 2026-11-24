#
# This source file is part of the Alexandria Chemistry Toolkit.
#
# Copyright (C) 2026
#
# Developers:
#             Mohammad Mehdi Ghahremanpour,
#             Paul J. van Maaren,
#             David van der Spoel (Project leader)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA  02110-1301, USA.
#
# Installation path for ACT python code. Depends from CMAKE_INSTALL_PREFIX.
# The directory site-packages/act, where the modules were until version 1.9b,
# belongs to the Python package act of ACT now.
set(ACT_PYTHON_SITE_PATH ${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_PYTHON_LIBDIR})
set(ACT_PYTHON_LIB_PATH ${ACT_PYTHON_SITE_PATH}/act_utilities)

# Configure 'sys.path' in the executable scripts, so they may find the library.
configure_file(gauss2molprop.cmakein gauss2molprop @ONLY)
configure_file(generate_mp.cmakein generate_mp @ONLY)
configure_file(mol_csv_api.py.cmakein mol_csv_api.py @ONLY)
configure_file(molselect.cmakein molselect @ONLY)
configure_file(reshuffle_selection.cmakein reshuffle_selection @ONLY)
configure_file(coords2molprop coords2molprop @ONLY)
configure_file(donchev2molprop donchev2molprop @ONLY)
configure_file(ncia2molprop ncia2molprop @ONLY)

# The modules of an installation with the earlier layout would be found
# before the new ones, and act.py there would hide the package act of ACT.
# Remove the files that the earlier versions installed, and only those.
set(ACT_OLD_MODULES
    act.py act_gct.py act_openmm.py actutils.py atomic_heat_of_formation.py
    dofit.py elements.py gaff_to_alexandria.py get_csv_rows.py get_mol_dict.py jacobi.py
    mol_csv_api.py mol_json.py molprops.py molutils.py
    ncia_reader_from_xyz.py read_gaussian_log.py)
configure_file(remove_old_layout.cmake.in remove_old_layout.cmake @ONLY)
install(SCRIPT ${CMAKE_CURRENT_BINARY_DIR}/remove_old_layout.cmake)

# Library scripts. The class ACT was in act.py, the name of the package of
# ACT; that package offers it as act.legacy.ACT.
install(FILES act_legacy.py DESTINATION ${ACT_PYTHON_LIB_PATH})
install(FILES act_gct.py DESTINATION ${ACT_PYTHON_LIB_PATH})
install(FILES act_openmm.py DESTINATION ${ACT_PYTHON_LIB_PATH})
install(FILES actutils.py DESTINATION ${ACT_PYTHON_LIB_PATH})
install(FILES atomic_heat_of_formation.py DESTINATION ${ACT_PYTHON_LIB_PATH})
install(FILES dofit.py DESTINATION ${ACT_PYTHON_LIB_PATH})
install(FILES elements.py DESTINATION ${ACT_PYTHON_LIB_PATH})
install(FILES get_csv_rows.py DESTINATION ${ACT_PYTHON_LIB_PATH})
install(FILES get_mol_dict.py DESTINATION ${ACT_PYTHON_LIB_PATH})
install(FILES jacobi.py DESTINATION ${ACT_PYTHON_LIB_PATH})
install(FILES mol_json.py DESTINATION ${ACT_PYTHON_LIB_PATH})
install(FILES molprops.py DESTINATION ${ACT_PYTHON_LIB_PATH})
install(FILES molutils.py DESTINATION ${ACT_PYTHON_LIB_PATH})
install(FILES ncia_reader_from_xyz.py DESTINATION ${ACT_PYTHON_LIB_PATH})
install(FILES read_gaussian_log.py DESTINATION ${ACT_PYTHON_LIB_PATH})
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/mol_csv_api.py DESTINATION ${ACT_PYTHON_LIB_PATH})

# Executable scripts
install(PROGRAMS ${CMAKE_CURRENT_BINARY_DIR}/gauss2molprop DESTINATION bin)
install(PROGRAMS ${CMAKE_CURRENT_BINARY_DIR}/generate_mp DESTINATION bin)
install(PROGRAMS ${CMAKE_CURRENT_BINARY_DIR}/molselect DESTINATION bin)
install(PROGRAMS ${CMAKE_CURRENT_BINARY_DIR}/reshuffle_selection DESTINATION bin)
install(PROGRAMS ${CMAKE_CURRENT_BINARY_DIR}/coords2molprop DESTINATION bin)
install(PROGRAMS dimer_scan DESTINATION bin)
install(PROGRAMS plot_convergence DESTINATION bin)
install(PROGRAMS view_fitness DESTINATION bin)
install(PROGRAMS ${CMAKE_CURRENT_BINARY_DIR}/donchev2molprop DESTINATION bin)
install(PROGRAMS ${CMAKE_CURRENT_BINARY_DIR}/ncia2molprop DESTINATION bin)
# The file act_utilities.pth adds the directory of the modules to the path
# of a Python that has this site-packages, such as that of a conda
# environment, also when its Python version differs from the one found here.
file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/act_utilities.pth "act_utilities\n")
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/act_utilities.pth
        DESTINATION ${ACT_PYTHON_SITE_PATH})

# Utilities that need no configuration
install(PROGRAMS annealing_plot.py calc_tip4p_dummy.py energy_distributions replace_interactions
        DESTINATION bin)


# Tests of the python scripts. The test of the OpenMM interface needs
# alexandria, from the PATH or the environment variable ACT_ALEXANDRIA,
# OpenMM, and the test data of ACT in the environment variable ACT_TESTDATA,
# and is skipped without them; the test of coords2molprop is skipped
# if RDKit cannot be imported.
if(BUILD_TESTING)
    add_test(NAME ActOpenMMTest
             COMMAND ${Python3_EXECUTABLE} -m unittest -v test_act_openmm
             WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/tests)
    add_test(NAME Coords2MolpropTest
             COMMAND ${Python3_EXECUTABLE} -m unittest -v test_coords2molprop
             WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/tests)
endif()
