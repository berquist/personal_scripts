#!/bin/bash

# Crudely reformat our starting PDB file for AMBER's leap.
# $1: pdb input
# $2: pdb output
# To use `reduce`, module load amber/12-intel

#  1. remove all hydrogens
#  2. make sure we are using Unix newlines
#  3. delete trailing whitespace from all lines
#  4. delete 2nd line that amber reduce inserts
#  5. change the histidine naming format from HSE, HSD (GROMACS) to HIE, HID (AMBER)
#  6. rename delta carbons on lysine residues
#  7. rename delta carbons on isoleucine residues
#  8. change the water naming format from TIP3W to WAT or HOH
#  9. rename the oxygens in the waters
# 10. rename the copper "residue"

#`which sed` -r -e '/^[123]?H/d' $1 > $2
#`which sed` -r -e '/[123]?H[ABDEGZ]?[123]?/d' $1 > $2
reduce -Trim $1 > $2
dos2unix $2
`which sed` -i -e 's/[ \t]*$//' $2
`which sed` -i -e '1d' $2
`which sed` -i -e 's/HS/HI/g' $2
`which sed` -i -e 's/CD1 LYS/CD  LYS/g' $2
`which sed` -i -e 's/CD  ILE/CD1 ILE/g' $2
`which sed` -i -e 's/TIP3W/WAT  /g' $2
`which sed` -i -e 's/OH2 WAT/O   WAT/g' $2
`which sed` -i -e 's/CU  CU /CU  CUA/g' $2

# Things that are missing:
# 1. change copper, water type from ATOM to HETATM
# 2. adding TER cards in the proper places
# 3. removing 5' terminal phosphate groups from DNA (P, O1P, O2P, O5' at the
#    beginning of each DNA chain) or charged phosphates
# 4. 
# For now, do manually
