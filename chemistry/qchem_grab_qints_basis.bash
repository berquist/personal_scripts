#!/usr/bin/env bash

output=basis_cgto.txt

# This doesn't work for UHF!
# TODO how so?
sed -n "/-- qints basis --/,/-- end of qints basis --/p" < "${1}" > ${output}
sed -i '1d;$d' ${output}
