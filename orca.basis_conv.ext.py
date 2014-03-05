#!/usr/bin/python

import argparse

"""orca.basis_conv.ext.py: Convert a GAMESS-US formatted basis file from EMSL
into something usable by ORCA as an external basis."""

parser = argparse.ArgumentParser()
parser.add_argument('inp_filename')
parser.add_argument('out_filename')
args = parser.parse_args()
inp_filename = args.inp_filename
out_filename = args.out_filename

inp_file = open(inp_filename, 'r')
inp_file_raw = inp_file.readlines()
inp_file.close()

# filter out unwanted lines
inp_file = [line.split() for line in inp_file_raw]
inp_file = [line for line in inp_file if line != []]
inp_file = [line for line in inp_file if line[0] != '!']
inp_file = [line for line in inp_file if line[0][0] != '$']

out_file = open(out_filename, 'w')
basis_name = inp_file_raw[0].split()[1]
print >> out_file, basis_name

for index, line in enumerate(inp_file):
    # There are 3 types of lines we must handle:
    # 1. Those that contain an element name (HYDROGEN, CARBON, COPPER, etc.) [length == 1]
    # 2. Those that contain shell info (S 3, L 1, etc.) [length == 2]
    # 3. Those that contain primitives (3 columns, first is an integer) [length >= 3]
    if len(line) == 1:
        print >> out_file, '{}'.format(*line)
    if len(line) == 2:
        print >> out_file, ' {} {}'.format(*line)
    if len(line) == 3:
        print >> out_file, '  {} {} {}'.format(*line)
    if len(line) == 4:
        print >> out_file, '  {} {} {} {}'.format(*line)

print >> out_file, 'STOP'

out_file.close()
