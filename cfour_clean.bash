#!/usr/bin/env bash

cfour_files=(
    basinfo.data
    den.dat
    fort.81
    fort.82
    fort.83
    ERREX
    FILES
    IIII
    IIJJ
    IJIJ
    IJKL
    JAINDX
    JMOLplot
    JOBARC
    MOL
    MOLDEN
    NEWMOS
    NTOTAL
    OLDMOS
)

for cfour_file in ${cfour_files[@]}; do
    rm ${cfour_file}
done
