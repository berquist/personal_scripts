#!/usr/bin/env bash

# match_inputs_and_outputs.sh: For each input file, is there a
# matching output file? Print out names of queue submission files that
# would create missing outputs.

inputfiles=$(ls *.in)

for inputfile in ${inputfiles[@]}; do
    outputfile=${inputfile//\.in/\.out}
    pbsfile=${inputfile//\.in/\.pbs}
    if [ ! -e ${outputfile} ]; then
        echo ${pbsfile}
    fi
done
