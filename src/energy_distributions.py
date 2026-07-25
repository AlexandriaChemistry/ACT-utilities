#!/usr/bin/env python3

import argparse, json, math, os, sys, xmltodict
import matplotlib.pyplot as plt
import numpy as np

debug       = False
fragments   = "fragments"
experiments = 'experiments'
atoms       = "atoms"

def parseArguments():
    desc = '''This script will read a json file produced by ACT train_ff.
It will then produce one or more violin plots showing the energy deviation
from the QM reference in multiple energy bins.
'''
    parser = argparse.ArgumentParser(description=desc)
 
    parser.add_argument("-f", "--infile", help="The json input file", type=str, default=None)
    parser.add_argument("-mp", "--molprop", help="Molprop file to extract dimer distances corresponding to the energies in the json file.", type=str, default=None)
    defout = "energy"
    parser.add_argument("-o", "--outfile", help="Output file. The extension will be removed and the name of the compound appended. Default "+defout, type=str, default=defout)
    parser.add_argument("-mol", "--molecule", help="Molecule or dimer, default is all", type=str, default=None)
    defwidth = 5
    parser.add_argument("-bw", "--binwidth", help="Width of histogram bins, kJ/mol for energies, Angstrom for distances, default "+str(defwidth), type=float, default=defwidth)
    defcmp = "EPOT"
    parser.add_argument("-cmp", "--component", help="Energy component to plot, default "+defcmp, type=str, default=defcmp)
    return parser.parse_args()

def get_coordinates(xmlfn:str)->dict:
    # Read molprop file
    coord = {}
    with open(xmlfn) as fd:
        doc = xmltodict.parse(fd.read())
    mols = "molecules"
    if not mols in doc:
        sys.exit("No %s in %s" % ( mols, infile ))
    mol = "molecule"
    nmols = len(doc[mols][mol])
    print("Number of molecules in molprop file %d" % nmols)
    exp       = "experiment"
    molprops = {}
    for m in range(nmols):
        molprop = {}
        for k in doc[mols][mol][m].keys():
            if fragments == k:
                molprop[fragments] = []
                for ff in doc[mols][mol][m][k]:
                    molprop[fragments].append(doc[mols][mol][m][k][ff])
            if exp == k:
                myexps = doc[mols][mol][m][k]
                if isinstance(myexps, dict):
                    myexps = [ myexps ]
                myexperiments = {}
                for me in myexps:
                    if debug:
                        print("me: {}".format(me))
                    myexperiment = {}
                    myatoms = []
                    for n in me:
                        if debug:
                            print("We have {}".format(n))
                        if n == "atom":
                            for a in me[n]:
                                if debug:
                                    print("a {}".format(a))
                                newat = { "@atomid": a["@atomid"], "@name": a["@name"] }
                                for xyz in [ 'x', 'y', 'z' ]:
                                    newat[xyz] = float(a[xyz])
                                myatoms.append(newat)
                        else:
                            continue
                    myexperiment[atoms] = myatoms
                    myexperiments[me['@datafile']] = myexperiment
                molprop[experiments] = myexperiments
        molprops[doc[mols][mol][m]['@molname']] = molprop
    return molprops
    
def make_energy_bin(mol:dict, outfile:str, binwidth:float, component:str):
    # First determine the minimum and maximum energy
    emin = None
    emax = None
    for calc in mol["interaction_energies"]:
        epot = float(mol["interaction_energies"][calc]["EPOT"]["QM"])
        if not emin or epot < emin:
            emin = epot
        if not emax or epot > emax:
            emax = epot
    # Then make the histogram
    nbins = 1+int((emax-emin)/binwidth)
    msd   = [None]*nbins
    # and fill it
    for calc in mol["interaction_energies"]:
        epot  = float(mol["interaction_energies"][calc]["EPOT"]["QM"])
        index = int((epot-emin)/binwidth)
        if component in mol["interaction_energies"][calc]:
            qm  = float(mol["interaction_energies"][calc][component]["QM"])
            act = float(mol["interaction_energies"][calc][component]["ACT"])
            if not msd[index]:
                msd[index] = []
            msd[index].append(act - qm)
    # Now plot it
    fig, axs =  plt.subplots(nrows=1, ncols=1, figsize=(9, 4))
    msd_np   = []
    xticks   = []
    for i in range(nbins):
        if msd[i]:
            msd_np.append(np.array(msd[i]))
            xticks.append("%.0f" % (emin+(i)*binwidth) )
    
    vpener   = axs.violinplot(msd_np, showmeans=False, showmedians=True)
    axs.yaxis.grid(True)
    axs.set_xticks([y for y in range(len(msd_np))], labels=xticks)
    axs.set_xlabel(f'{component} (kJ/mol)')
    axs.set_ylabel(f'Residual (ACT-QM)')
    axs.set_title(mol["name"])
    plt.show()

def compute_dist(atoms: list, frags:list):
    dmin = 1e8
    for ii in frags[0]['#text'].split():
        i = int(ii)-1
        for jj in frags[1]['#text'].split():
            j = int(jj)-1
            d2 = 0
            for xyz in [ 'x', 'y', 'z' ]:
                d2 += (atoms[i][xyz]-atoms[j][xyz])**2
            d1 = math.sqrt(d2)
            if d1 < dmin:
                dmin = d1
    return dmin

def make_dist_bin(mol:dict, outfile:str, binwidth:float, component:str, molprop):
    # Zero, start with check
    if not mol['name'] in molprop:
        print("Molecule/dimer %s not present in the molprop file" % mol['name'])
        return
    # First determine the distance
    mp    = molprop[mol['name']]
    frags = mp[fragments][0]
    if len(frags) != 2:
        print("Computing distance does not make sense when there are %d fragments" % (len(frags)))
        return
    dist_data = {}
    dmin = 1e8
    dmax = 0
    for exper in mp[experiments].keys():
        myatoms = mp[experiments][exper][atoms]
        mydist  = compute_dist(myatoms, frags)
        dindex  = f"calculation-{exper}"
        dist_data[dindex] = mydist
        dmin = min(dmin, mydist)
        dmax = max(dmax, mydist)

    # Then make the histogram
    nbins = 1+int((dmax-dmin)/binwidth)
    msd   = [None]*nbins
    # and fill it
    for calc in mol["interaction_energies"]:
        epot  = float(mol["interaction_energies"][calc]["EPOT"]["QM"])
        if calc in dist_data:
            index = int((dist_data[calc]-dmin)/binwidth)
            if component in mol["interaction_energies"][calc]:
                qm  = float(mol["interaction_energies"][calc][component]["QM"])
                act = float(mol["interaction_energies"][calc][component]["ACT"])
                if not msd[index]:
                    msd[index] = []
                msd[index].append(act - qm)
    # Now plot it
    fig, axs =  plt.subplots(nrows=1, ncols=1, figsize=(9, 4))
    msd_np   = []
    xticks   = []
    for i in range(nbins):
        if msd[i]:
            msd_np.append(np.array(msd[i]))
            xticks.append("%.1f" % (dmin+(i)*binwidth) )
    
    vpener   = axs.violinplot(msd_np, showmeans=False, showmedians=True)
    axs.yaxis.grid(True)
    axs.set_xticks([y for y in range(len(msd_np))], labels=xticks)
    axs.set_xlabel('Distance ($\\mathrm{\\AA}$)')
    axs.set_ylabel(f'Residual {component} (ACT-QM)')
    axs.set_title(mol["name"])
    plt.show()
        
if __name__ == "__main__":
    args  = parseArguments()
    if not args.infile or not os.path.exists(args.infile):
        sys.exit("Please provide a valid input file name")
    if args.binwidth <= 0:
        sys.exit("Binwidth should be positive")
    with open(args.infile, "r") as inf:
        train_data = json.load(inf)
    if not "train_ff" in train_data or not "molecules" in train_data["train_ff"]:
        sys.exit("Something wrong with input file %s" % args.infile)
    molprop = None
    if args.molprop:
        molprop = get_coordinates(args.molprop)
    for mol in train_data["train_ff"]["molecules"]:
        if not args.molecule or train_data["train_ff"]["molecules"][mol]["name"] == args.molecule:
            if molprop:
                make_dist_bin(train_data["train_ff"]["molecules"][mol],
                              args.outfile, args.binwidth, args.component, molprop)
            else:
                make_energy_bin(train_data["train_ff"]["molecules"][mol],
                                args.outfile, args.binwidth, args.component)
