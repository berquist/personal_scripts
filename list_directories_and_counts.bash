#!/bin/bash

for dir in $(find * -maxdepth 0 -type d); do
    echo "${dir}" $(ls "${dir}" | wc -w)    
done
