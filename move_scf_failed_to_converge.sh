#!/usr/bin/env bash

# move_scf_failed_to_converge.sh: ...

searchstr="SCF failed to converge"
target_folder="scf_failed_to_converge"

results=$(grep -l "${searchstr}" *.out)

for output in ${results[@]}; do
    mv ${output} ${target_folder}
    input=${output//\.out/\.in}
    mv ${input} ${target_folder}
    echo ${input}
done
