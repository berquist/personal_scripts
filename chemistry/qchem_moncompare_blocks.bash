#!/usr/bin/env bash

# run "moncompare.csh -v" on output files in the current dir, only printing
# when the comparison to the reference failed

set -uo pipefail

export QCPLATFORM=LINUX_Ix86_64

for outputfilename in *.out; do
    contents=$(moncompare.csh -v "${outputfilename}")
    if [[ $? != 0 ]]; then
        echo "${contents}"
    fi
done
