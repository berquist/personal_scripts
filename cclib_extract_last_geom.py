#!/usr/bin/env python

import argparse
import os.path
from cclib.parser import ccopen
from cclib.parser.utils import PeriodicTable

parser = argparse.ArgumentParser()
parser.add_argument('qmoutfiles', nargs = '+')
parser.add_argument('--suffix')
args = parser.parse_args()
qmoutfiles = args.qmoutfiles
suffix = args.suffix

pt = PeriodicTable()

for qmoutfile in qmoutfiles:

    job = ccopen(qmoutfile)
    data = job.parse()
    last_geometry = data.atomcoords[-1]
    element_list = [pt.element[Z] for Z in data.atomnos]

    stub = os.path.splitext(qmoutfile)[0]
    if suffix:
        xyzfilename = ''.join([stub, '.', suffix, '.xyz'])
    else:
        xyzfilename = ''.join([stub, '.xyz'])

    s = '{:3s} {:15.10f} {:15.10f} {:15.10f}'

    with open(xyzfilename, 'w') as xyzfile:
        xyzfile.write(str(len(last_geometry)) + '\n')
        xyzfile.write('\n')
        for atom, atomcoords in zip(element_list, last_geometry):
            xyzfile.write(s.format(atom, *atomcoords) + '\n')

    print(xyzfilename)
