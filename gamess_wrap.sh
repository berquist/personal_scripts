#!/bin/bash

# gamess_wrap.sh: Handle some of the dirty stuff when running a GAMESS
# calculation.

# Run gamess using the following commands:
#     rungms input_file version_no cpu_num > result.log
# such as:
#     rungms test.inp 01 6 > test.log

ppn="${1}"
input="${2}"

stub="${input%.*}"
scrdir="${HOME}"/scr

exts=(
    dat
    trj
    rst
    efp
)

for ext in ${exts[@]}; do
    rm "${scrdir}/${stub}.${ext}"
done

$(which rungms) "${input}" 01 "${ppn}" > "${stub}".out
