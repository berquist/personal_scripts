#!/usr/bin/env bash

inputs=$(ls *mm.in)

for input in ${inputs[@]}; do
    echo "${input}"
    sed -i '/ideriv/d' "${input}"
done
