#!/usr/bin/env bash

# qchem_remove_guess_coefficients.bash: Old versions of the
# fragment/EDA liked to print the block diagonal MO coefficients T
# before entering SCF(MI) without a way to turn it off...delete that
# section.

for filename in "$@"; do

    echo "${filename}"

    # This of course assumes no linear dependencies, so nbasis == nmo!
    nbasis=$(sed -nr "s/There are [1-9][0-9]* shells and ([1-9][0-9]*) basis functions$/\1/p" < "${filename}")
    start_alpha=$(grep -n "Guess Alpha MO Coefficients" "${filename}" | cut -d " " -f 1 | tr -d ":")
    start_beta=$(grep -n "Guess Beta  MO Coefficients" "${filename}" | cut -d " " -f 1 | tr -d ":")
    len_section=$((${start_beta} - ${start_alpha}))
    stop_alpha=$((${start_beta} - 1))
    stop_beta=$((${start_beta} + ${len_section} - 1))
    next_line=$((${stop_beta} + 1))

    sed -i -e "${start_alpha},${stop_alpha}d" -e "${start_beta},${stop_beta}d" "${filename}"

done
