#!/usr/bin/env bash

# qchem_move_completed_calcs.sh: Move completed calculations (both
# inputs and outputs) to the specified folder (second argument).

destdir="${2}"
mkdir -p "${destdir}"

outputs=$(find . -type f -name "*.out")

# This is how many times the search string needs to show up for a
# calculation to be considered "completed".
count_for_completed="${1}"
searchstr='Thank you very much for using Q-Chem'

for output in ${outputs[@]}; do
    count=$(grep -c "${searchstr}" "${output}")
    if [ "${count}" -eq "${count_for_completed}" ]; then
        stub="${output%.*}"
        mv -v ${stub}.* "${destdir}"
    fi
done
