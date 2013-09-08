#!/bin/bash

# $1: pdbinputfile
# $2: pdbfile_nohydrogens

`which awk` '($3 !~ /^[123]?H/ ){print}' $1 > $2