#
# This source file is part of the Alexandria Chemistry Toolkit.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
"""
Build hook of hatchling that makes the wheel of act-utilities for PyPI with
the same layout as the installation with CMake (src/CMakeLists.txt and
share/CMakeLists.txt):

- the modules in site-packages/act_utilities, with the file
  act_utilities.pth that puts this directory on the path of Python;
- the scripts in the bin directory of the environment;
- the data files in share/act of the environment, where actutils.actdata()
  and alexandria find them.

CMake writes the directory of the modules into a few scripts. The wheel does
not know where it will be installed, and does not need to: the file
act_utilities.pth puts the modules on the path. The line is replaced by a
comment.

The lists below must stay the same as those of the CMakeLists.txt files;
the workflow pypi.yml compares the two installations.
"""
import os
import shutil
import tempfile
from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

## The modules, from src
MODULES = [
    "act_legacy.py", "act_gct.py", "act_openmm.py", "actutils.py",
    "atomic_heat_of_formation.py", "dofit.py", "elements.py",
    "get_csv_rows.py", "get_mol_dict.py", "jacobi.py", "mol_json.py",
    "molprops.py", "molutils.py", "ncia_reader_from_xyz.py",
    "read_gaussian_log.py", "mol_csv_api.py.cmakein",
]

## The scripts, from src
SCRIPTS = [
    "gauss2molprop.cmakein", "generate_mp.cmakein", "molselect.cmakein",
    "reshuffle_selection.cmakein", "coords2molprop", "dimer_scan",
    "plot_convergence", "view_fitness", "donchev2molprop", "ncia2molprop",
    "annealing_plot.py", "calc_tip4p_dummy.py", "energy_distributions",
    "replace_interactions",
]

## The data files, from share
DATA = [
    "alexandria.json", "atom_bond.xml", "atomization-energies-dft.csv",
    "atomization-energies.csv", "atomprops.csv", "excluded_molecules.csv",
    "vsite2_halogen_sigma_holes.json", "vsite2_water_sigma_holes.json",
    "vsite3_alcohol_bisector.json", "vsite3_alcohol_lone_pairs.json",
    "vsite3_water_bisector.json", "vsite3_water_lone_pairs.json",
    "vsite4_amine.json",
]

## What CMake replaces in the scripts and modules, and what replaces it here
PATH_LINE = 'sys.path.insert(1, "@ACT_PYTHON_LIB_PATH@")'
PATH_COMMENT = "# The file act_utilities.pth puts the modules of ACT-utilities on the path"


class CustomBuildHook(BuildHookInterface):
    """Puts the modules, scripts and data files in the wheel."""

    def _configured(self, source: Path, target: Path) -> Path:
        """Copy a file without the directory of the modules that CMake writes in it.
        @param source The file in src.
        @param target The copy.
        @return The copy.
        """
        text = source.read_text(encoding="utf-8")
        if "@" in text.replace(PATH_LINE, ""):
            # Another variable of CMake would stay in the file
            for line in text.splitlines():
                if "@ACT_" in line or "@CMAKE_" in line:
                    raise ValueError("%s: cannot configure '%s'" % (source, line.strip()))
        target.write_text(text.replace(PATH_LINE, PATH_COMMENT), encoding="utf-8")
        target.chmod(source.stat().st_mode)
        return target

    def initialize(self, version, build_data):
        """Add the files to the wheel.
        @param version    The kind of wheel, standard or editable.
        @param build_data What goes into the wheel.
        """
        if self.target_name != "wheel":
            return
        root = Path(self.root)
        src = root / "src"
        # Not in the output directory, where the wheel goes
        self._work = tempfile.mkdtemp(prefix="act-utilities-")
        work = Path(self._work)

        pth = work / "act_utilities.pth"
        pth.write_text("act_utilities\n", encoding="utf-8")
        build_data["force_include"][str(pth)] = "act_utilities.pth"
        for name in MODULES:
            installed = name.removesuffix(".cmakein")
            copy = self._configured(src / name, work / installed)
            build_data["force_include"][str(copy)] = "act_utilities/" + installed
        scripts = work / "bin"
        scripts.mkdir(exist_ok=True)
        for name in SCRIPTS:
            installed = name.removesuffix(".cmakein")
            copy = self._configured(src / name, scripts / installed)
            build_data["shared_scripts"][str(copy)] = installed
        for name in DATA:
            build_data["shared_data"][os.fspath(root / "share" / name)] = "share/act/" + name

    def finalize(self, version, build_data, artifact_path):
        """Remove the copies once the wheel is written.
        @param version       The kind of wheel.
        @param build_data    What went into the wheel.
        @param artifact_path The wheel.
        """
        work = getattr(self, "_work", None)
        if work:
            shutil.rmtree(work, ignore_errors=True)
