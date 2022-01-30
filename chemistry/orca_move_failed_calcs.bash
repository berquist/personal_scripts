#!/usr/bin/env bash

# orca_move_failed_calcs.sh: Find incomplete or failed ORCA
# calculations and move all files related to the calculation to a
# separate folder.

destdir=incomplete
mkdir -p "${destdir}"

# assume everything is an ORCA output!
outputs=$(find . -type f -name "*.out")

# This is how many times the search string needs to show up for a
# calculation to be considered "completed".
count_for_completed=1
searchstr='****ORCA TERMINATED NORMALLY****'

for output in ${outputs[@]}; do
    count=$(grep -c "${searchstr}" "${output}")
    if [ "${count}" -ne "${count_for_completed}" ]; then
        stub="${output%.*}"
        mv -v ${stub}.* "${destdir}"
    fi
done
