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

    conda install -c conda-forge alexandria

which installs this package, `act-utilities`, as well. On its own:

    conda install -c conda-forge act-utilities

From source, before building ACT, into the prefix where ACT will be
installed, or into the conda environment used for ACT:

    cmake -S . -B build -DCMAKE_INSTALL_PREFIX=<prefix>
    cmake --install build

The modules go to `<prefix>/lib/pythonX.Y/site-packages/act`, the scripts
to `<prefix>/bin` and the data files to `<prefix>/share/act`. A Python that
uses this site-packages, such as that of a conda environment, finds the
modules through the file `act.pth`; otherwise
`source <prefix>/bin/ACTRC` of ACT adds them to `PYTHONPATH`.

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

    rattler-build build --recipe conda/recipe.yaml --channel conda-forge
