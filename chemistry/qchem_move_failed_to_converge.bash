#!/usr/bin/env bash

# qchem_move_failed_to_converge.sh: Find Q-Chem calculations that
# failed to converge the energy and move all files related to the
# calculation to a separate folder.

destdir="${1}"
mkdir -p "${destdir}"

# assume everything is an Q-Chem output!
outputs=$(find . -maxdepth 1 -type f -name "*.out")

# This signifies the calculation has finished, but the SCF didn't
# converge.
searchstr='SCF failed to converge'

for output in ${outputs[@]}; do
    count=$(tail "${output}" | grep -c "${searchstr}")
    if [ "${count}" -eq 1 ]; then
        stub="${output%.*}"
        mv -v ${stub}.* "${destdir}"
    fi
done
