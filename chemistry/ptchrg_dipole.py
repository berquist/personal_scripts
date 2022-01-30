#!/usr/bin/env python

"""ptchrg_dipole.py: Given a file of ORCA point charges, calculate
their collective dipole moment."""


import numpy as np


def ptchrg_dipole(namein):

    with open(namein) as handle:
        contents = handle.readlines()

    # the format is similar to a real XYZ file,
    # where the element symbol is instead the charge in a.u.
    n = int(contents[0].strip())
    comment = contents[1].strip()
    charges = [charge.strip().split() for charge in contents[2:]]

    # calculate the centroid (geometrical center) of the point charges
    centroid = np.zeros(3)
    for charge in charges:
        centroid[0] += float(charge[1])
        centroid[1] += float(charge[2])
        centroid[2] += float(charge[3])
    centroid /= n
    print("centroid:", centroid)

    # find the relative position of each charge to the centroid,
    # then calculate the dipole
    total = 0.0
    dipole = np.zeros(3)
    for charge in charges:
        total += float(charge[0])
        # print "charge, total:", float(charge[0]), total
        position = np.array([float(charge[1]), float(charge[2]), float(charge[3])])
        rel = position - centroid
        dipole += float(charge[0]) * rel

    print("total charge:", total)
    print("dipole:", dipole)
    norm = np.linalg.norm(dipole)
    print("||dipole||:", norm)
    dipolenorm = dipole / norm
    print("dipole (unit):", dipolenorm)

    return (total, dipole, norm, dipolenorm)


if __name__ == "__main__":
    import argparse as ap

    parser = ap.ArgumentParser()
    parser.add_argument("namein", metavar="<ptchrg xyz file>", default="ptchrg.xyz")
    args = parser.parse_args()
    namein = args.namein

    ptchrg_dipole(namein)
