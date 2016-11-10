#!/usr/bin/env python

# Drives many-body calculations.
# The script uses Q-Chem to do the actual quantum chemical calculations and
# extracts energies and gradients.

import argparse
import sys

###
# Read user input
###

parser = argparse.ArgumentParser(description='This script drives many-body (MB) expansion calculations using Q-Chem.')
parser.add_argument('fxyz', metavar='<xyz file>',
                   help='the XYZ coordinate file of the total system')
parser.add_argument('fscf', metavar='<SCF template>',
                   help='Q-Chem input template for the SCF run')
parser.add_argument('fmp2', metavar='<MP2 template>',
                   help='Q-Chem input template for the MP2 run')
parser.add_argument('-n', type=int, default=2,
                   help='maximum order of the MB expansion (default: 2)')
parser.add_argument('-mono', type=int, default=0,
                   help='number of atoms per monomer ')

args = parser.parse_args()

# Assign user input to internal variables
Nmax = args.n
fXYZName = args.fxyz
fSCFName = args.fscf
fMP2Name = args.fmp2
# TODO: Check validity of user input



###
# Welcome screen

print """
=======================================================================
 MANY-BODY EXPANSION TO ORDER N
======================================================================="""

print """
We'll perform an MB expansion of the correlation energy:
Etot = ESCF + Ecorr(MBn) """

print """
-----------------------------------------------------------------------
INPUT PARAMETERS
-----------------------------------------------------------------------"""
print "XYZ input: ", fXYZName
print "SCF template: ", fSCFName
print "MP2 template: ", fMP2Name
print "Maximum MB order: ", Nmax
print "-----------------------------------------------------------------------"
print
###



# For now we assume that the system is made up of monomers of the same size.
# Ask the user to specify the number of atoms per monomer, so we can determine
# which atoms belong to which monomer.
NAtom_per_frag = args.mono
while NAtom_per_frag <= 0:
    NAtom_per_frag = int( raw_input("How many atoms per monomer? ") )

print "Number of atoms per fragment is ", NAtom_per_frag



# Reads XYZ coordinates of supersystem
print "Reading XYZ file ..."
fXYZ = open(fXYZName, 'r')
NAtom = int( fXYZ.readline() )
print "  Number of atoms: ", NAtom
Comment = fXYZ.readline()
#print "  Comment line: \"", Comment, "\""
XYZ = []
for line in fXYZ:
    #print line
    for word in line.split():
        XYZ.append(word)


# Determines the total number of fragments
Nfrag = NAtom / NAtom_per_frag
print "Number of fragments: ", Nfrag
# TODO: Check if the XYZ input is consistent with the assumption that we're
# dealing with identical fragments.


# Splits XYZ coordinates into monomers
# TODO


# Calculates the energy of the supersystem
print "Calculating the SCF energy of the supersystem ..."
ESCF = 0.0
# TODO

# Calculates the MB-expanded correlation energy
print "Calculating the MB-expanded correlation energy ..."
Ecorr_MB2 = 0.0

for i in range(Nfrag):
    for j in range(i+1,Nfrag):
        print "  Calculating Dimer ", i, "-", j, "..."
        eij = 0.0
        Ecorr_MB2 += eij


# Calculates the total energy
Etot = ESCF + Ecorr_MB2
print "Total Energy: ", Etot, " a.u."


### Classes
class Monomer:
    """A monomer."""
    XYZ = []


### Interfaces to Q-Chem

def getEnergy(Monomers, Method):
    """ Calculates the energy of an n-mer.
    The n-mer and desired method are specified as arguments.
    """
    energy = 0.0
    return energy

def getGradient(Monomers, Method):
    """ Calculates the nuclear gradient of an n-mer.
    The n-mer and desired method are specified as arguments.
    """
    return 0
