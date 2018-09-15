#!/usr/bin/env bash

# manipulate_rem.sh: ...

new_rem_lines=" scf_max_cycles = 1000\n chelpg = false\n molden_format = false"

inputs=$(ls *.in)

for input in ${inputs[@]}; do
    sed -i "s/\$rem/\$rem\n${new_rem_lines}/" ${input}
done
