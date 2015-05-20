#!/usr/bin/env bash

inputs=$(ls *.in)

for input in ${inputs[@]}; do
    output=${input//in/out}
    qchem -nt 4 ${input} ${output}
done
