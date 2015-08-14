#!/usr/bin/env bash

# move_completed_calcs.sh: Move complete calculations (both inputs and
# outputs) to the specified folder (first argument).

destdir="${1}"
mkdir -p "${destdir}"

outputs=$(ls *.out)

# This is how many times the search string needto show up for a
# calculation to be considered "completed".
count_for_completed=6

searchstr='Have a nice day'

for output in ${outputs[@]}; do
    count=$(grep -c "${searchstr}" "${output}")
    if [ ${count} = ${count_for_completed} ]; then
        input="${output//out/in}"
        mv -v "${input}" "${destdir}"
        mv -v "${output}" "${destdir}"
    fi
done
