#!/usr/bin/env python

# Given a PDB file (ambpdb output) and an atom number, find the
# "maximum internal distance" inside the protein.

import argparse as ap
import numpy as np
import itertools

parser = ap.ArgumentParser()
parser.add_argument('namein',  metavar='<input PDB file>')
parser.add_argument('startid', metavar='<atom index>')

args = parser.parse_args()
locals().update(vars(args))

handle   = open(namein, 'r')
contents = handle.readlines()

# Assume the very first entry is an ATOM, and that we only have extra
# TER and END cards.
atoms = [atom.strip().split() for atom in contents]

# Remove the TER and END cards
iterator = itertools.compress(atoms, [((atom[0] != 'TER') and (atom[0] != 'END')) for atom in atoms])
atoms = list(iterator)

# Search for the starting atom
for atom in atoms:
    if (atom[1] == startid):
        startcoords = np.array([float(atom[5]), float(atom[6]), float(atom[7])])
        print "start:", startid, patom

maxdist = 0.0
idx = 0
match = []
# Calculate all the pairwise distances, and keep the largest
for atom in atoms:
    currentid = atom[1]
    coords = np.array([float(atom[5]), float(atom[6]), float(atom[7])])
    diff = np.linalg.norm(coords - startcoords)
    if diff > maxdist:
        maxdist = diff
        idx = currentid
        match = atom

print "end:", idx, match, maxdist
