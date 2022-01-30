#!/usr/bin/env python

"""qchem.extract_mc_geometries.py: Extract all the geometries present
from a QCT-AIMD job where:
 aimd_qct_which_trajectory = -n and
 aimd_qct_initpos = -n."""


import argparse
import os.path

parser = argparse.ArgumentParser()
parser.add_argument("mcoutfilename")
args = parser.parse_args()
mcoutfilename = args.mcoutfilename
stubfilename = os.path.splitext(mcoutfilename)[0]

print("Reading geometries from {}".format(mcoutfilename))

geometries = []

# Read all the geometries from the output file.
with open(mcoutfilename) as mcoutfile:
    for line in mcoutfile:
        # Assume that the number of geometries generated matches
        # the number of trajectories being averaged over.
        if "Vibrational distribution with " in line:
            ntrajectories = int(line.split()[3])
            print("Number of geometries: {}".format(ntrajectories))
        if "Geometry #" in line:
            while "Nuclear coordinates (a.u.):" not in line:
                line = next(mcoutfile)
            line = next(mcoutfile)
            geometry = []
            while line != "\n":
                atomcoords = line.split()
                geometry.append(atomcoords)
                line = next(mcoutfile)
            geometries.append(geometry)

zfill = len(str(ntrajectories))

# Write all the geometries to individual Cartesian XYZ files (in Angstrom).
for i, geometry in enumerate(geometries):
    xyzfilename = ".".join([stubfilename, str(i + 1).zfill(zfill), "xyz"])
    with open(xyzfilename, "w") as xyzfile:
        xyzfile.write(str(len(geometry)) + "\n")
        xyzfile.write("\n")
        for atom in geometry:
            atom[1:] = map(lambda x: float(x) * 0.52917721, atom[1:])
            # pylint: disable=W0142
            xyzfile.write("{:3} {} {} {}\n".format(*atom))
    # print('Wrote {}.'.format(xyzfilename))

print("Wrote {} XYZ files.".format(ntrajectories))
