#!/usr/bin/env bash

nthreads=${1:-1}

inputs=$(ls *.in)

for input in ${inputs[@]}; do
    output=${input//in/out}
    qchem -nt "${nthreads}" "${input}" "${output}"
done

# can also do:
# for f in *.in; do stub=${f%.in}; qchem ${stub}.in ${stub}.out; done
