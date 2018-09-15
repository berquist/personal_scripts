#!/usr/bin/env bash

# qchem_cppcheck.sh: ...

cppcheck --enable=all --language=c++ --std=c++03 ./*.C ./*.h
