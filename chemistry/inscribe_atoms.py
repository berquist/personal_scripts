#!/usr/bin/env python

# Given an XYZ file, find the radius of the smallest sphere that will
# surround all the atoms.

import argparse as ap
import numpy as np
import itertools

parser = ap.ArgumentParser()
parser.add_argument("namein", metavar="<input XYZ file>")
args = parser.parse_args()
# namein = args.namein
locals().update(vars(args))

handle = open(namein, "r")
contents = handle.readlines()

n = int(contents[0].strip())
comment = contents[1].strip()
atoms = [atom.strip().split() for atom in contents[2:]]

# Calculate the pairwise distance between every atom. The largest
# distance wil be the diameter of the sphere.
maxdist = 0.0
origin = np.empty(3)
for i in range(0, n):
    for j in range(i + 1, n):
        ivec = np.array([float(atoms[i][1]), float(atoms[i][2]), float(atoms[i][3])])
        jvec = np.array([float(atoms[j][1]), float(atoms[j][2]), float(atoms[j][3])])
        dist = np.linalg.norm(ivec - jvec)
        if dist > maxdist:
            maxdist = dist
            origin = (ivec + jvec) / 2

print("radius:", maxdist / 2)
print("origin:", origin)
