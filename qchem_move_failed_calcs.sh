#!/usr/bin/env bash

# qchem_move_failed_calcs.sh: Find incomplete or file Q-Chem calculations
# and move all files related to the calculation to a separate folder.

destdir=incomplete
mkdir -p "${destdir}"

outputs=$(find . -maxdepth 1 -type f -name "*.out")

# This is how many times the search string needs to show up for a
# calculation to be considered "completed".
count_for_completed="${1}"
searchstr='Thank you very much for using Q-Chem'

for output in ${outputs[@]}; do
    count=$(grep -c "${searchstr}" "${output}")
    if [ "${count}" -ne "${count_for_completed}" ]; then
        stub="${output%.*}"
        mv -v ${stub}.* "${destdir}"
    fi
done
