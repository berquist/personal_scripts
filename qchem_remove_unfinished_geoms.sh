#!/usr/bin/env bash

# qchem_remove_unfinished_geoms.sh: If any XYZ files are present that
# correspond to incomplete geometry optimizations, delete them.

# This only works in folders that only contain Q-Chem outputs!

outputs=$(ls *.out)

for output in ${outputs[@]}; do
    ret=$(grep -L "Have a nice day" ${output})
    if [[ ${ret} != "" ]]; then
        xyzfile=${ret//\.out/\.xyz}
        echo ${xyzfile}
        rm ${xyzfile}
    fi
done
