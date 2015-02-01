#!/usr/bin/env python

# Given a file of numbers, extract those (atoms|residues) from a PDB file
# and create an XYZ file from them.

import argparse as ap
import numpy as np
import itertools

parser = ap.ArgumentParser()
parser.add_argument('namein',  metavar='<input PDB file>')
parser.add_argument('resfile', metavar='<(atom|residue) file>')

args = parser.parse_args()
locals().update(vars(args))

pdbhandle = open(namein, 'r')
contents  = pdbhandle.readlines()

# Assume the very first entry is an ATOM, and that we only have extra
# TER and END cards.
atoms = [atom.strip().split() for atom in contents]

# Remove the TER and END cards
iterator = itertools.compress(atoms, [((atom[0] != 'TER') and (atom[0] != 'END')) for atom in atoms])
atoms = list(iterator)

# Read in the number file and store them in a list
reshandle = open(resfile, 'r')
contents  = reshandle.readlines()
residues = [residue.strip() for residue in contents]

# Find and collect the appropriate atoms for each residue
collect = []
for residue in residues:
    # Residue numbers are in the 5th column
    for atom in atoms:
        if atom[4] == residue:
            collect.append(atom)

# Convert into XYZ format; assume that the 11th column is the element, and
# the 6/7/8 columns are the x, y, z coords
xyzhandle = open(namein + '.xyz', 'w')
print >> xyzhandle, len(collect)
print >> xyzhandle, ''
for atom in collect:
    print >> xyzhandle, "%-2s %12.5e %12.5e %12.5e" % (
        atom[10], float(atom[5]), float(atom[6]), float(atom[7]))
print >> xyzhandle, ''

pdbhandle.close()
reshandle.close()
xyzhandle.close()
