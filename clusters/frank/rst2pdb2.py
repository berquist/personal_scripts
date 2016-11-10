#!/usr/bin/env python

"""rst2pdb.py: Convert a series of Amber restart files into a PDB trajectory, so a geometry optimization can be observed."""

import os
import glob
import re
import argparse

"""Here is the help string for 'ambpdb' which does the real work for us:

ambpdb -h

Usage:
ambpdb [OPTION]... < restrt > out.pdb

Options:
 -p PRMTOP     Define PRMTOP filename (default:"prmtop").
 -tit TITLE    Write a REMARK record containing TITLE.
                   (default: use prmtop title)
 -aatm         Left-justified Amber atom names.
 -bres         Brookhaven Residue names (HIE->HIS, etc.).
 -ctr          Center molecule on (0,0,0).
 -noter        Do not write TER records.
 -ext          Use PRMTOP extended PDB info, if present.
 -ene FLOAT    Define H-bond energy cutoff for FIRST.
 -bin          The coordinate file is in binary form.
 -offset INT   Add offset to residue numbers.

Options for alternate output format (give only one of these):
 -pqr          PQR (MEAD) format with charges and radii.
 -sas          PQR with 1.4 added to atom radii.
 -mol2         TRIPOS MOL2 format.
 -bnd          list bonds from the PRMTOP.
 -atm          Mike Connolly surface/volume format.
 -first        Add REMARKs for input to FIRST.
"""

# ambpdb -p his.top < amber.rst > amber.pdb

# We will call ambpdb like this:
# ambpdb -p {prmtop} < {infile}.rst_{idx} >> {outfile}.pdb

# Variables that we will need:
# - name of the topology file
# - indices, starting and ending, default to none (just the {infile}.rst)
# - root name of the input files
# - root name of the output PDB file, default to same as root of input
# This amounts to 5 CLI-specified variables

# in the future, when not testing, the user must cd to the directory they want
# to work in before running the script
#os.chdir('/home/dlambrecht/erb74/qmmm/amber/02d_pm3_full_orca_from00_trap/rst')
#args = 'his.top -i 0 -f 10 amber amber'

parser = argparse.ArgumentParser(description='keep herping that derp')
parser.add_argument('prmtop',
                    metavar='<topology file>',
                    help='')
parser.add_argument('-i',
                    dest='idxstart',
                    metavar='<starting index>',
                    type=int,
                    default=0,
                    help='')
parser.add_argument('-f',
                    dest='idxend',
                    metavar='<ending index>',
                    type=int,
                    default=None,
                    help='')
parser.add_argument('namein',
                    metavar='<input base name>',
                    help='')
parser.add_argument('nameout',
                    metavar='<output base name>',
                    help='')

#args = parser.parse_args(args.split())
args = parser.parse_args()

prmtop   = args.prmtop
idxstart = args.idxstart
idxend   = args.idxend
namein   = args.namein
nameout  = args.nameout

rsts = glob.glob('{}.rst*'.format(namein))

# the sorting function will fail later if encouters the 1st file, which
# doesn't end with the underscore/integer
if rsts[0] == '{}.rst'.format(namein):
    os.system("mv {0}.rst {0}.rst_0".format(namein))

def sort_func(string):
    return int(string.strip().split('_')[-1])

# sort the files by integer (0, 1, 3, 30, 200, etc.) in place
rsts.sort(key = sort_func)

i = rsts.index('{}.rst_{}'.format(namein, idxstart))
f = rsts.index('{}.rst_{}'.format(namein, idxend))

ohandle = open('{}.pdb'.format(nameout), 'w')
for rst in rsts[i:f+1]:
    print("ambpdb -p {} < {} >> {}.pdb".format(prmtop, rst, nameout))
    os.system("ambpdb -p {} < {} >> {}.pdb".format(prmtop, rst, nameout))
