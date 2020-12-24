#!/usr/bin/env bash

# gamess_wrap.bash: Handle some of the dirty stuff when running a GAMESS
# calculation.

# Run gamess using the following commands:
#     rungms input_file version_no cpu_num > result.log
# such as:
#     rungms test.inp 01 6 > test.log

ppn="${1}"
input="${2}"

stub="${input%.*}"
scrdir=/tmp

exts=(
    dat
    trj
    rst
    efp
)

for ext in ${exts[@]}; do
    rm "${scrdir}/${stub}.${ext}"
done

$(command -v rungms) "${input}" 00 "${ppn}" > "${stub}".out

mv "${scrdir}/${stub}.dat" .
