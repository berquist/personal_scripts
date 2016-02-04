#!/bin/bash

# cfour_wrap.sh: 

# Strip off the file extension to get the root name of the
# calculation.
stub=${1%.*}
ext=${1##*.}

# CFOUR needs to run in its own directory.
mkdir ${stub}
cd ${stub}
cp ../${stub}.${ext} ./ZMAT
ln -s ${CFOUR_ROOT}/basis/GENBAS .
xcfour > ${stub}.out
cd ..
