#!/usr/bin/env bash

# qchem_move_incomplete_geoms.sh: Find incomplete Q-Chem geometry
# optimizations that otherwise terminated normally (just ran out of
# cycles) and move all files related to the calculation to a separate
# folder.

destdir="${1}"
mkdir -p "${destdir}"

# assume everything is an Q-Chem output!
outputs=$(find . -maxdepth 1 -type f -name "*.out")

# This signifies the calculation has finished, but the geometry
# optimization didn't converge in time.
searchstr='MAXIMUM OPTIMIZATION CYCLES REACHED'

for output in ${outputs[@]}; do
    count=$(tail "${output}" | grep -c "${searchstr}")
    if [ "${count}" -eq 1 ]; then
        stub="${output%.*}"
        mv -v ${stub}.* "${destdir}"
    fi
done
