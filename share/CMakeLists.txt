# The data files of ACT that the Python tools and alexandria use. They are
# installed with those of ACT, in share/act, where alexandria finds them;
# ACT also looks here if ACT-utilities is installed in another prefix.
install(FILES
        alexandria.json
        atom_bond.xml
        atomtype_mapping.csv
        atomization-energies-dft.csv
        atomization-energies.csv
        atomprops.csv
        excluded_molecules.csv
        vsite2_halogen_sigma_holes.json
        vsite2_water_sigma_holes.json
        vsite3_alcohol_bisector.json
        vsite3_alcohol_lone_pairs.json
        vsite3_water_bisector.json
        vsite3_water_lone_pairs.json
        vsite4_amine.json
        DESTINATION share/act)
