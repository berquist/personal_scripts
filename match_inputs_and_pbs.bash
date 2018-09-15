#!/usr/bin/env bash

# match_inputs_and_pbs.sh: For each input file, is there a matching
# batch system submission script? Print out names of inputs with
# missing scheduler submission scripts.

inputfiles=$(ls *.in)

for inputfile in ${inputfiles[@]}; do
    pbsfile=${inputfile//\.in/\.pbs}
    if [ ! -e ${pbsfile} ]; then
        echo ${inputfile}
    fi
done
