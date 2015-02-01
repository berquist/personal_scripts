#!/usr/bin/env python

"""Given a MOPAC-style z-matrix created by Molden, reformat it for use by ORCA."""

import argparse

parser = argparse.ArgumentParser(description="")
parser.add_argument(dest="mopacfname", metavar="<MOPAC-formatted Z-matrix filename>", type=str, help="")
parser.add_argument(dest="orcafname", metavar="<ORCA-formatted Z-matrix filename>", type=str, help="")

args = parser.parse_args()

mopacfname = args.mopacfname
orcafname = args.orcafname

mopacfile = open(mopacfname, "r")
mopaccontents = mopacfile.readlines()
mopacfile.close()

orcafile = open(orcafname, "w")

s = "{:3s} {:3d} {:3d} {:3d} {:12.7f} {:12.7f} {:12.7f}"

for line in mopaccontents[3:-1]:
    entry = line.split()
    # ordering: element symbol, 3 connectivities, bond length, angle, dihedral
    symb = entry[0]
    con1 = int(entry[7])
    con2 = int(entry[8])
    con3 = int(entry[9])
    par1 = float(entry[1])
    par2 = float(entry[3])
    par3 = float(entry[5])
    print >> orcafile, s.format(symb, con1, con2, con3, par1, par2, par3)

orcafile.close()
