#!/usr/bin/env bash

# match_inputs_and_outputs.sh: For each input file, is there a
# matching output file? Print out names of input files that would
# create missing outputs.

inputfiles=$(ls *.in)

for inputfile in ${inputfiles[@]}; do
    outputfile=${inputfile//\.in/\.out}
    if [ ! -e ${outputfile} ]; then
        echo ${inputfile}
    fi
done
