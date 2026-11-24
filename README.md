# ACT-utilities

Python modules and scripts for the
[Alexandria Chemistry Toolkit (ACT)](https://github.com/AlexandriaChemistry/ACT):
pre- and post-processing, converters to molprop files, the interface to
OpenMM, and analysis tools. ACT requires them. Until ACT 1.9b they were in
`src/act/python` of the ACT repository, see `src/README.md` for the list.

The data files that these tools use, and that `alexandria` reads as well,
such as `alexandria.json`, `atom_bond.xml` and `atomprops.csv`, are in
`share` and are installed in `<prefix>/share/act`.

## Installation

With conda, together with ACT:

    conda install -c alexandriachemistry -c conda-forge alexandria

which installs this package, `act-utilities`, as well. On its own:

    conda install -c alexandriachemistry -c conda-forge act-utilities

With pip, from PyPI, into a virtual environment or another Python
environment of your own:

    pip install act-utilities

This installs the same files as conda and CMake: the modules in
`site-packages/act_utilities` with the file `act_utilities.pth`, the scripts
in the `bin` directory of the environment and the data files in its
`share/act`. Use the environment that ACT is installed in, or set the
environment variable `ACTDATA` to the data files, so that `alexandria` finds
them. ACT itself, with the Python package `act`, is not on PyPI; install it
with conda or from source.

From source, before building ACT, into the prefix where ACT will be
installed, or into the conda environment used for ACT:

    cmake -S . -B build -DCMAKE_INSTALL_PREFIX=<prefix>
    cmake --install build

The modules go to `<prefix>/lib/pythonX.Y/site-packages/act_utilities`, the
scripts to `<prefix>/bin` and the data files to `<prefix>/share/act`. A
Python that uses this site-packages, such as that of a conda environment,
finds the modules through the file `act_utilities.pth`; otherwise
`source <prefix>/bin/ACTRC` of ACT adds them to `PYTHONPATH`.

Until version 1.9b the modules were in `site-packages/act`. That directory
is now the Python package `act` of ACT, the interface to the `alexandria`
program. Installing this version removes the files of the earlier layout
from the same prefix. The module `act.py` with the class `ACT` has the name
`act_legacy.py` now; use `from act.legacy import ACT` with ACT installed, or
`from act_legacy import ACT`.

## Tests

    cd build && ctest

The test of the OpenMM interface needs `alexandria`, from the `PATH` or the
environment variable `ACT_ALEXANDRIA`, OpenMM, and the test data of ACT,
the directory `src/act/testdata` of its source code, in the environment
variable `ACT_TESTDATA`. It is skipped without them, unless
`ACT_REQUIRE_OPENMM` is set; the CI of ACT runs it.

## Conda package

`conda/recipe.yaml` builds the package with
[rattler-build](https://rattler.build):

    rattler-build build --recipe conda/recipe.yaml \
        --channel alexandriachemistry --channel conda-forge

The workflow `.github/workflows/conda.yml` does this for pull requests
that change the recipe or what is installed. It uploads the package to the
channel `alexandriachemistry` on anaconda.org for a tag `v` plus the
version in the recipe, with the label `main`, and for a run by hand (Actions,
Conda package, Run workflow, with Upload ticked) with the label that is
given, `dev` by default:

    conda install -c alexandriachemistry/label/dev -c conda-forge act-utilities

A file that is on the channel is not replaced. For a new build of the same
version, raise `build: number` in the recipe first; a new version starts
again at 0. The package `alexandria` of ACT asks for the `act-utilities` of
its own version.

## PyPI package

`pyproject.toml` and the build hook `hatch_build.py` make the sdist and the
wheel of `act-utilities` for PyPI:

    python -m build

The wheel has the layout of the installation with CMake, and
`hatch_build.py` has the lists of modules, scripts and data files of
`src/CMakeLists.txt` and `share/CMakeLists.txt`: add a new file to both.
The workflow `.github/workflows/pypi.yml` builds and tests the package for
pull requests, compares its files with those that CMake installs, and
publishes it on PyPI for a tag `v` plus the version, through trusted
publishing. The version in `pyproject.toml` must be that of
`conda/recipe.yaml`.
