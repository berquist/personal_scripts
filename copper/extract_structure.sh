#!/bin/bash

source /etc/profile.d/modules.sh
module purge
module load amber/12-tools13-intel2013

# this should remove all hydrogen from the protein, plus all the solvent and ions
  full_mask="!(@H= | :WAT,Na+)"

# save as above, but keep the hydrogens
  fullh_mask="!(:WAT,Na+)"

# let's just pick the residues and remove the backbone stuff, it's much less ambiguous
# active_mask="@1-1519,1522-1523,1525,1527-1528,1530-2401,2404,2407-3565,3568,3571-9045,9072,9075,9078"
  active_mask="((:98,154,229,549)&!(@CA,C,O,N,H=))"

# still remove backbone and alpha hydrogens
  activeh_mask="((:98,154,229,549)&!(@CA,C,O,N,H,HA))"

# Ozan's active site; dump the 
  ozan_mask="((:98,154,229,549)&!(@CA,C,O,N,H,HA,))"
  ozanh_mask=""

echo "Full protein (no hydrogens, water/solvent, Na+)"
full="ambmask -p 1e1a.prmtop -c $1 -out pdb -find \"$full_mask\" >& ${1}_full.pdb"
echo "${full}"
eval $full
echo ""

echo "Full protein with hydrogens (no water/solvent, Na+)"
fullh="ambmask -p 1e1a.prmtop -c $1 -out pdb -find \"$fullh_mask\" >& ${1}_fullh.pdb"
echo "${fullh}"
eval $fullh
echo ""

echo "Active site (no hydrogens):"
active="ambmask -p 1e1a.prmtop -c $1 -out pdb -find \"$active_mask\" >& ${1}_active.pdb"
echo "${active}"
eval $active
echo ""

echo "Active site (with hydrogens):"
activeh="ambmask -p 1e1a.prmtop -c $1 -out pdb -find \"$activeh_mask\" >& ${1}_activeh.pdb"
echo "${activeh}"
eval $activeh
echo ""

activehwat3_mask="(((:98,154,229,549 <:3.0) & :WAT)&!(@CA,C,O,N,H,HA))"

echo "Active site (with hydrogens and waters w/in 3 Angstroms):"
activehwat3="ambmask -p 1e1a.prmtop -c $1 -out pdb -find \"$activehwat3_mask\" >& ${1}_activehwat3.pdb"
echo "${activehwat3}"
eval $activehwat3
echo ""