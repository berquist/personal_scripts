#!/bin/bash

output=basis.txt

# This doesn't work for UHF!
sed -n "/--- qints basis ---/,/--- end of qints basis ---/p" < "${1}" > ${output}
sed -i '1d;$d' ${output}
