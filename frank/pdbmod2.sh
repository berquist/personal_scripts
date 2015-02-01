#!/usr/bin/env bash

# Crudely reformat our starting PDB file for AMBER's leap
# $1: pdb input
# $2: pdb output

`which sed` -r -e '/^[123]?H/d' $1 > $2
#`which sed` -r -e '/[123]?H[ABDEGZ]?[123]?/d' $1 > $2
reduce -Trim $1 > $2
`which sed` -i -e 's/HS/HI/g' $2
`which sed` -i -e 's/CD  LYS/CD1 LYS/g' $2
`which sed` -i -e 's/TIP3W/HOH  /g' $2
