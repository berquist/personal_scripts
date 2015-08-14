#!/usr/bin/env python

"""cclib_extract_last_geom.py: Extract the last geometry from a
quantum chemical output file (not just geometry optimization) using
cclib. Name is the same stub, with the file extension replaced by
'.xyz'.
"""

from __future__ import print_function
import argparse
import os.path
from cclib.parser import ccopen
from cclib.parser.utils import PeriodicTable


# pylint: disable=C0103
parser = argparse.ArgumentParser()
parser.add_argument('qmoutfiles', nargs='+')
parser.add_argument('--suffix')
args = parser.parse_args()
qmoutfiles = args.qmoutfiles
suffix = args.suffix

pt = PeriodicTable()

s = '{:3s} {:15.10f} {:15.10f} {:15.10f}'

for qmoutfile in qmoutfiles:

    job = ccopen(qmoutfile)
    try:
        data = job.parse()
    # this is to deal with the Q-Chem parser not handling incomplete
    # SCF cycles properly
    except StopIteration:
        print('no output made: StopIteration in {}'.format(qmoutfile))
        continue
    # pylint: disable=E1101
    last_geometry = data.atomcoords[-1]
    element_list = [pt.element[Z] for Z in data.atomnos]

    stub = os.path.splitext(qmoutfile)[0]
    if suffix:
        xyzfilename = ''.join([stub, '.', suffix, '.xyz'])
    else:
        xyzfilename = ''.join([stub, '.xyz'])

    with open(xyzfilename, 'w') as xyzfile:
        xyzfile.write(str(len(last_geometry)) + '\n')
        xyzfile.write('\n')
        for atom, atomcoords in zip(element_list, last_geometry):
            # pylint: disable=W0142
            xyzfile.write(s.format(atom, *atomcoords) + '\n')

    print(xyzfilename)
