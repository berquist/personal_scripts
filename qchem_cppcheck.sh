#!/bin/sh

# qchem_cppcheck.sh: ...

cppcheck --enable=all --std=c++03 ./*.C ./*.h
