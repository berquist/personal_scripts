#!/usr/bin/env python

"""cclib_extract_last_geom.py: Extract the last geometry from any
quantum chemical output file (not just geometry optimizations) using
cclib. Name is the same stub, with the file extension replaced by
'.xyz'.
"""

from __future__ import print_function
import argparse
import os.path
import cclib
from cclib.parser import ccopen
from cclib.parser.utils import PeriodicTable


# pylint: disable=C0103
parser = argparse.ArgumentParser()
parser.add_argument('qmoutfiles', nargs='+')
parser.add_argument('--suffix')
parser.add_argument('--fragment', action='store_true')
args = parser.parse_args()
qmoutfiles = args.qmoutfiles
suffix = args.suffix

pt = PeriodicTable()

s = '{:3s} {:15.10f} {:15.10f} {:15.10f}'

for qmoutfile in qmoutfiles:

    job = ccopen(qmoutfile)
    try:
        data = job.parse()
    except Exception as e:
        print('no output made: {} in {}'.format(e, qmoutfile))
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
            xyzfile.write(s.format(atom, *atomcoords) + '\n')
        print(xyzfilename)

    if args.fragment:
        # If this is from a Q-Chem fragment calculation, print a single
        # fragment "XYZ" file as well.
        if isinstance(job, cclib.parser.qchemparser.QChem):
            with open(qmoutfile) as fh:
                charges = []
                multiplicities = []
                start_indices = []
                line = ''
                while '$molecule' not in line:
                    line = next(fh)
                line = next(fh)
                sys_charge, sys_multiplicity = line.split()
                counter = -1
                # Gather the charges, spin multiplicities, and starting
                # positions of each fragment.
                while '$end' not in line:
                    if '--' in line:
                        line = next(fh)
                        charge, multiplicity = line.split()
                        charges.append(charge)
                        multiplicities.append(multiplicity)
                        start_indices.append(counter)
                        line = next(fh)
                    else:
                        counter += 1
                        line = next(fh)
            assert len(charges) == len(multiplicities) == len(start_indices)
            if suffix:
                fragxyzfilename = ''.join([stub, '.', suffix, '.xyz_frag'])
            else:
                fragxyzfilename = ''.join([stub, '.xyz_frag'])
            with open(fragxyzfilename, 'w') as fh:
                t = '{:3} {:15.10f} {:15.10f} {:15.10f}'.format
                blocks = []
                blocks.append('{} {}'.format(sys_charge, sys_multiplicity))
                from itertools import count
                for (charge, multiplicity, idx_iter) in zip(charges, multiplicities, count(0)):
                    blocks.append('--')
                    blocks.append('{} {}'.format(charge, multiplicity))
                    idx_start = start_indices[idx_iter]
                    try:
                        idx_end = start_indices[idx_iter + 1]
                    except IndexError:
                        idx_end = len(element_list)
                    for atomsym, atomcoords in zip(element_list[idx_start:idx_end], last_geometry[idx_start:idx_end]):
                        blocks.append(t(atomsym, *atomcoords))
                fh.write('\n'.join(blocks))
                print(fragxyzfilename)
