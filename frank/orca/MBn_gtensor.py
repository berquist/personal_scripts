#!/usr/bin/env python

import argparse
import subprocess
import os.path

# """MBn_gtensor.py: Given a set of XYZ files that are individual fragments of a system, do a many-body expansion of the g-tensor and compare to the full system."""

# parser = argparse.ArgumentParser()
# parser.add_argument('fxyz', nargs='+')
# args = parser.parse_args()
# args = parser.parse_args(sp.check_output(["ls", "~/calc.epr/mbe/frag\*.xyz"]))
# fxyzlist = args.fxyz
fxyzlist = [
    "/home/dlambrecht/erb74/calc.epr/mbe/frag1.xyz",
    "/home/dlambrecht/erb74/calc.epr/mbe/frag2.xyz",
    "/home/dlambrecht/erb74/calc.epr/mbe/frag3.xyz",
    "/home/dlambrecht/erb74/calc.epr/mbe/frag4.xyz",
    "/home/dlambrecht/erb74/calc.epr/mbe/frag5.xyz",
    "/home/dlambrecht/erb74/calc.epr/mbe/frag6.xyz",
    "/home/dlambrecht/erb74/calc.epr/mbe/frag7.xyz"
]

nmax = len(fxyzlist)

def eprfile(charge, multiplicity, xyzfile):
    """
    A default template for an EPR input file.
    """
    return """! uks pbe0 def2-tzvpp def2-tzvpp/jk ri rijk pmodel somf(1x) noautostart tightscf grid5

%pal
 nprocs 1
 end

* xyzfile {0} {1} {2}.xyz *

%eprnmr
 tol 1e-10
 gtensor 1
 ori centerofelcharge
 printlevel 5
 end

""".format(charge, multiplicity, xyzfile)

def pbsfile(xyzfile):
    """
    A default template for a PBS job file.
    """
    return """#!/bin/bash

#PBS -N {0}
#PBS -q shared
#PBS -l nodes=1:ppn=1
#PBS -l walltime=144:00:00
#PBS -j oe
#PBS -l qos=low
#PBS -m abe
#PBS -M erb74@pitt.edu

module purge
module load intel/2013.0
module load openmpi/1.6.5-intel12
module load orca/3.0.1

cp $PBS_O_WORKDIR/{0}.inp $LOCAL
cp $PBS_O_WORKDIR/{0}.xyz $LOCAL
cd $LOCAL

run_on_exit() {{
    set -v
    cp $LOCAL/* $PBS_O_WORKDIR
}}

trap run_on_exit EXIT

$(which orca) {0}.inp >& $PBS_O_WORKDIR/{0}.out
""".format(xyzfile)

class Fragment:
    """
    A fragment is a molecule that can be combined with another
    fragment.
    """
    def __init__(self):
        self.fxyz = ""
        self.name = ""
        self.charge = 0
        self.multiplicity = 1
        self.symbols = []
        self.coords = []
        self.nfragments = 0

    def read(self, fxyz):
        """
        Load the charge, multiplicity, and coordinates into the fragment.
        """
        self.fxyz = fxyz
        self.name = os.path.splitext(os.path.basename(fxyz))[0]
        xyzhandle = open(fxyz, "r")
        xyzhandle.readline()
        self.charge, self.multiplicity = map(int, xyzhandle.readline().split())
        raw_coords = xyzhandle.readlines()
        xyzhandle.close()
        for line in raw_coords:
            if line != '\n':
                self.symbols.append(line.split()[0])
                self.coords.append(map(float, line.split()[1:]))
        self.nfragments += 1

    def write(self, fxyz):
        """
        Write an XYZ file to disk, with the charge and multiplicity stored
        in the comment line.
        """
        xyzhandle = open(fxyz, "w")
        s = "{:2s} {:f} {:f} {:f}"
        for symbol, coords in zip(self.symbols, self.coords):
            print >> xyzhandle, s.format(symbol, *coords)
        xyzhandle.close()

    def __str__(self):
        return self.name

    def __add__(self, other):
        return self.combine(other)

    def combine(self, other):
        """
        Combine this fragment with another fragment, returning a new fragment.
        """
        new = Fragment()
        new.name = other.name + self.name
        new.charge = other.charge + self.charge
        if other.multiplicity == self.multiplicity:
            new.multiplicity = 1
        else:
            new.multiplicity = 2
        new.symbols = other.symbols + self.symbols
        new.coords = other.coords + self.coords
        new.nfragments = other.nfragments + self.nfragments
        return new

    def combine_write(self, other, fxyz):
        """
        Combine this fragment with another fragment, returning a new fragment
        and writing it to disk.
        """
        new = self.combine(other)
        new.write(fxyz)
        return new

def is_active(f):
    """
    Determine of the combination of fragments in the given iterable
    are EPR-active (doublet, not singlet).
    """
    active = False
    for fragment in f:
        if fragment.multiplicity == 2:
            active = not active
    return active

def combine(x, y):
    """
    Combine two fragments into one, returning a new fragment.
    """
    new = Fragment()
    new.name = x.name + y.name
    new.charge = x.charge + y.charge
    if x.multiplicity == y.multiplicity:
        new.multiplicity = 1
    else:
        new.multiplicity = 2
    new.symbols = x.symbols + y.symbols
    new.coords = x.coords + y.coords
    new.nfragments = x.nfragments + y.nfragments
    return new

def combine(f):
    """
    Combine multiple fragments into one, returning a new fragment.
    """
    new = Fragment()
    for fragment in f:
        new.name += fragment.name
        new.charge += fragment.charge
        if new.multiplicity == fragment.multiplicity:
            new.multiplicity = 1
        else:
            new.multiplicity = 2
        new.symbols += fragment.symbols
        new.coords += fragment.coords
        new.nfragments += fragment.nfragments
    return new

def combine_write(x, y, fxyz):
    """
    Combine two fragments into one, returning a new fragment
    and writing it to disk.
    """
    new = combine(x, y)
    new.write(fxyz)
    return new

def read_fragment_input(fraginp):
    """
    Parse the special fragment-type input, as seen in Q-Chem and Psi4.
    """
    pass

# generate the jobs for each of the individual fragments
# for fxyz in fxyzlist:
#     dir = os.path.dirname(fxyz)
#     stub = os.path.splitext(os.path.basename(fxyz))[0]
#     orcaname = stub + ".inp"
#     pbsname = stub + ".pbs"
#     orcahandle = open(os.path.join(dir, orcaname), "w")
#     pbshandle = open(os.path.join(dir, pbsname), "w")
#     print orcaname
#     print >> orcahandle, eprfile(charge, multiplicity, stub)
#     print pbsname
#     print >> pbshandle, pbsfile(stub)
#     orcahandle.close()
#     pbshandle.close()

def generate_monomers(fxyzlist):
    """
    Generate all the starting fragments (monomers) from coordinate files.
    """
    monomers = []
    for fxyz in fxyzlist:
        monomer = Fragment()
        monomer.read(fxyz)
        monomers.append(monomer)
    return monomers

def generate_dimers(m):
    """
    Generate all possible dimers from the list of monomers.
    """
    dimers = []
    n = len(m)
    for i in range(n):
        for j in range(i+1, n):
            dimers.append(combine(m[i], m[j]))
    return dimers

def generate_trimers(m):
    """
    Generate all possible trimers from the list of monomers.
    """
    trimers = []
    n = len(m)
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                trimers.append(combine(m[i], combine(m[j], m[k])))
    return trimers

def remove_inactive(f):
    """
    Return the list of fragments in f that are EPR active.
    """
    pass

def generate_two_body_terms(m):
    """
    """
    terms = set()
    n = len(m)
    for i in range(n):
        for j in range(i+1, n):
            pass
