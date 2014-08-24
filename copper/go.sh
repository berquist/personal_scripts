#!/bin/bash

source /etc/profile.d/modules.sh
module purge
module load amber/

wget http://www.rcsb.org/pdb/files/1q8n.pdb.gz
gunzip 1q8n.pdb.gz

#take out only one instance of the system
cat 1q8n.pdb| head -n 1407 > 1q8n_only_one_mgr.pdb

#grep out mg coordinates only
grep MGR 1q8n_only_one_mgr.pdb | grep HETATM > mgr.pdb

export AMBERHOME=/opt/amber-9.17

#ANTECHAMBER stuff
$AMBERHOME/exe/antechamber -i mgr.pdb -fi pdb -o mgr.prepi -fo prepi -c
bcc -s 2 -nc 1

$AMBERHOME/exe/parmchk -i mgr.prepi -f prepi -o mgr.frcmod

#LEAP Stuff

cat > leap.bat << EOF

source leaprc.gaff
source leaprc.rna.ff99
loadamberprep mgr.prepi
loadamberparams mgr.frcmod

addPdbAtomMap {
   { "H2*" "H2'1" }
}
mymol = loadpdb 1q8n_only_one_mgr.pdb

saveamberparm mymol mgrcomplex.prmtop mgrcomplex.inpcrd

quit

EOF

rm leap.log 