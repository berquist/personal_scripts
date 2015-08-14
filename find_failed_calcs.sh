#!/usr/bin/env bash

# find_failed_calcs.sh: ...

searchstr="Thank you very much for using Q-Chem"

results=$(grep -L "${searchstr}" *.out)

mkdir -p incomplete
for output in ${results[@]}; do
    stub="${output%.*}"
    for f in ${stub}.*; do
        mv -v "${f}" incomplete
    done
    # mv -v "${stub}.*" incomplete
done
