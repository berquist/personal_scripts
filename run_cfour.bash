#!/usr/bin/env bash

# run_cfour.bash: Handle some of the dirty stuff when running a CFOUR
# calculation.

# Strip off the file extension to get the root name of the
# calculation.
stub=${1%.*}
ext=${1##*.}

# CFOUR needs to run in its own directory. Make sure it doesn't exist
# before running.
rm -r ${stub}
mkdir ${stub}
cd ${stub}
cp ../${stub}.${ext} ./ZMAT
ln -s ${CFOUR_ROOT}/basis/GENBAS .
xcfour > ${stub}.out
cp ${stub}.out ..
cd ..
