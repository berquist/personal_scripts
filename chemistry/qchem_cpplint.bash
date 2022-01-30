#!/usr/bin/env bash

# qchem_cpplint.sh: Run cpplint with the correct settings to handle
# Q-Chem's C++ file extensions.

# If you don't want it to complain about header guard levels, run from
# $QC.
cpplint --root=. --extensions=C --headers=h ./*.C ./*.h
