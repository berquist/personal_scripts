#!/usr/bin/env python

"""cclib_extract_pointcharges.py: Extract point charges from a quantum
chemical output file (not just geometry optimization) using
cclib. Name is the same stub, with the file extension replaced by
'.txt'.

The format of the output is two columns, the first being the atomic
symbol, the second being the magnitude of the charge.
"""

from __future__ import print_function
import argparse
import os.path
from cclib.parser import ccopen
from cclib.parser.utils import PeriodicTable


parser = argparse.ArgumentParser()

parser.add_argument('qmoutfiles',
                    nargs='+')
parser.add_argument('--ptchrgtype',
                    choices=('mulliken', 'lowdin', 'chelpg', 'hirshfeld'),
                    default='mulliken')

args = parser.parse_args()
qmoutfiles = args.qmoutfiles

pt = PeriodicTable()

s = '{:3s} {:15.10f}'

for qmoutfile in qmoutfiles:

    job = ccopen(qmoutfile)
    data = job.parse()

    element_list = [pt.element[Z] for Z in data.atomnos]
    pointcharges = data.atomcharges[args.ptchrgtype]

    ptchrgfilename = ''.join([os.path.splitext(qmoutfile)[0], '.txt'])

    with open(ptchrgfilename, 'w') as ptchrgfile:
        for element, pointcharge in zip(element_list, pointcharges):
            ptchrgfile.write(s.format(element, pointcharge) + '\n')

    print(ptchrgfilename)
