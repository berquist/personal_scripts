#!/usr/bin/env bash

# qchem_find_failed_calcs.sh: Find incomplete or file Q-Chem
# calculations and echo the output names.

outputs=$(find . -type f -name "*.out")

# This is how many times the search string needs to show up for a
# calculation to be considered "completed".
count_for_completed="${1}"
searchstr='Thank you very much for using Q-Chem'

for output in ${outputs[@]}; do
    count=$(grep -c "${searchstr}" "${output}")
    if [ "${count}" -ne "${count_for_completed}" ]; then
        echo "${output}"
    fi
done
