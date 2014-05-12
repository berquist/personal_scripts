#!/usr/bin/env python

"""orca.basis_conv.ext.py: Convert a GAMESS-US formatted basis file from EMSL
into something usable by ORCA as an internal basis."""

import argparse
from periodic_table import sym2num

parser = argparse.ArgumentParser()
parser.add_argument('inp_filename')
parser.add_argument('out_filename')
args = parser.parse_args()
inp_filename = args.inp_filename
out_filename = args.out_filename

inp_file = open(inp_filename, 'rb')
inp_file_raw = inp_file.readlines()
inp_file.close()

# filter out unwanted lines
inp_file = [line.split() for line in inp_file_raw]
inp_file = [line for line in inp_file if line != []]
inp_file = [line for line in inp_file if line[0] != '!']
inp_file = [line for line in inp_file if line[0][0] != '$']

out_file = open(out_filename, 'wb')
basis_name = inp_file_raw[0].split()[1]
out_file.write('# ' + basis_name + '\n')

for index, line in enumerate(inp_file):
    # There are 3 types of lines we must handle:
    # 1. Those that contain an element name (HYDROGEN, CARBON, COPPER, etc.) [length == 1]
    # 2. Those that contain shell info (S 3, L 1, etc.) [length == 2]
    # 3. Those that contain primitives (3 columns, first is an integer) [length >= 3]
    if len(line) == 1:
        if index > 0:
            out_file.write(' end\n')
        out_file.write('{} {}\n'.format('newgto', sym2num[line[0]]))
    if len(line) == 2:
        out_file.write(' {} {}\n'.format(*line))
    if len(line) == 3:
        out_file.write('  {} {} {}\n'.format(*line))
    if len(line) == 4:
        out_file.write('  {} {} {} {}\n'.format(*line))

out_file.write(' end\n')

out_file.close()
