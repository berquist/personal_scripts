#!/usr/bin/env bash

inputs=$(ls *mm.in)

for input in ${inputs[@]}; do
    newfilename=${input//mm\.in/mm_analytic\.in}
    sed '/ideriv/d' < ${input} > ${newfilename}
done
