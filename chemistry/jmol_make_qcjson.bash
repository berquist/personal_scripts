#!/usr/bin/env bash

# jmol_make_qcjson.bash: Given a filename, convert to QCJSON/MolSSI QCSchema
# using Jmol.

stub=${1%.*}

cat <<EOF > "${stub}".spt
load ${1}
write ${stub}.qcjson
EOF

# jmol -onl ${stub}.spt
java -jar /usr/share/jmol/JmolData.jar -onl "${stub}".spt
rm "${stub}".spt
