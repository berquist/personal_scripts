#!/usr/bin/env python

import argparse

from orcaparse import orca_parser

# """MBn_gtensor2.py: ..."

fjoblist = [
    "/home/dlambrecht/erb74/calc.epr/mbe/frag1.out",
    "/home/dlambrecht/erb74/calc.epr/mbe/frag2.out",
    "/home/dlambrecht/erb74/calc.epr/mbe/frag3.out",
    "/home/dlambrecht/erb74/calc.epr/mbe/frag4.out",
    "/home/dlambrecht/erb74/calc.epr/mbe/frag5.out",
    "/home/dlambrecht/erb74/calc.epr/mbe/frag6.out",
    "/home/dlambrecht/erb74/calc.epr/mbe/frag7.out"
]

nmax = len(fjoblist)

for fjob in fjoblist:
    orcajob = orca_parser.ORCAOutputParser(fjob)
    gmatrix = orcajob.molecule.gtensor.gmatrix
