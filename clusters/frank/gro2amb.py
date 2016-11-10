#!/usr/bin/env python

import argparse
from itertools import compress

parser = argparse.ArgumentParser()
parser.add_argument('namein')
parser.add_argument('nameout')
args = parser.parse_args()

namein  = args.namein
nameout = args.nameout

# read the PDB file and clean it for parsing
inhandle = open(namein, 'r')
pdbfile  = inhandle.readlines()
pdbclean = []
for line in pdbfile:
    pdbclean.append(line.strip().split())

# 1. remove any entry that doesn't begin with ATOM, TER, or HETATM
# 2. remove any entry that contains a hydrogen in the 3rd column
# 3a. remove the 5th column from every entry  (idx 4)
# 3b. remove the 12th column from every entry (idx 11)
# 4a. set the 1st item in the 2nd column to 1, increment by 1 every entry
# 4b. set the 1st item in the 6th column to 1, increment by 1 every different residue
# 5. add 'END' at the very end

# 1
pdbclean[:] = [line for line in pdbclean if ((line[0] == 'ATOM') or
                                             (line[0] == 'TER') or
                                             (line[0] == 'HETATM'))]
# 2
pdbclean[:] = [line for line in pdbclean if line[-1] != 'H']
# 3
mask = [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0]
pdbmasked = []
for line in pdbclean:
    line_temp = []
    for field in compress(line, mask):
        line_temp.append(field)
    pdbmasked.append(line_temp)
pdbclean[:] = pdbmasked[:]
# 4
for i in range(len(pdbclean)):
    pdbclean[i][1] = i+1
# 5
pdbclean.append(['END'])

outhandle = open(nameout, 'w')
for line in pdbclean:
    for field in line:
        outhandle.write('%s\t' % field)
    outhandle.write('\n')

inhandle.close()
outhandle.close()

if __name__ == '__main__':
    print('namein:', namein)
    print('nameout:', nameout)
