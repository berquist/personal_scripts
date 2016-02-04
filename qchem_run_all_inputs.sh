#!/usr/bin/env bash

nthreads=${1:-1}

inputs=$(ls *.in)

for input in ${inputs[@]}; do
    output=${input//in/out}
    qchem -nt "${nthreads}" "${input}" "${output}"
done
