#!/usr/bin/env python

"""cclib_calc_com.py: Calculate the center of mass and center of
nuclear charge for the final geometry of one or more quantum chemical
output files (using cclib).
"""


def centerofmass(coords, masses):
    """Calculate the center of mass for the given coordinates and
    masses.
    """
    total_mass = sum(masses)
    mwc_x = masses * coords[:, 0]
    mwc_y = masses * coords[:, 1]
    mwc_z = masses * coords[:, 2]
    com_x = sum(mwc_x) / total_mass
    com_y = sum(mwc_y) / total_mass
    com_z = sum(mwc_z) / total_mass
    return (com_x, com_y, com_z)


def centerofnuccharge(coords, charges):
    """Calculate the center of mass for the given coordinates and
    charges.
    """
    total_mass = sum(charges)
    mwc_x = charges * coords[:, 0]
    mwc_y = charges * coords[:, 1]
    mwc_z = charges * coords[:, 2]
    com_x = sum(mwc_x) / total_mass
    com_y = sum(mwc_y) / total_mass
    com_z = sum(mwc_z) / total_mass
    return (com_x, com_y, com_z)


def main():
    """Parse a series of output files and print out the center of mass and
    canter of nuclear charge for the final geometry.
    """
    import argparse

    from cclib.io import ccopen
    from cclib.parser.utils import PeriodicTable

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="+")
    args = parser.parse_args()

    pt = PeriodicTable()
    for filename in args.filename:

        job = ccopen(filename)
        data = job.parse()

        # pylint: disable=E1101
        elementnums = data.atomnos
        # FIXME averaged mass
        elementmasses = [pt.Mass[pt.element[i]] for i in elementnums]
        coords = data.atomcoords[-1]

        print(elementnums)
        print(elementmasses)
        print(coords)
        print(centerofmass(coords, elementmasses))
        print(centerofnuccharge(coords, elementnums))


if __name__ == "__main__":

    main()
