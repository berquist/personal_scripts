#!/bin/bash

stub=${1%.*}

cat <<EOF > ${stub}.spt
load ${1}
write ${stub}.qcjson
EOF

# jmol -onl ${stub}.spt
java -jar /usr/share/jmol/JmolData.jar -onl ${stub}.spt
rm ${stub}.spt
