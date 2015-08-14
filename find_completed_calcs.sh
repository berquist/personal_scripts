#!/usr/bin/env bash

# find_completed_calcs.sh: ...

searchstr="Thank you very much for using Q-Chem"

# results=$(grep -l "${searchstr}" *.out)
results=$(find . -type f -name "*.out" -exec grep -l "${searchstr}" '{}' \;)

for output in ${results[@]}; do
    echo "${output}"
done
