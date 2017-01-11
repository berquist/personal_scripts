#!/bin/bash

# qchem_00_update_qcaux_qcref.sh
# Run this script (usually via cron) to update all the
# library files Q-Chem needs to run, as well as the reference outputs
# used for testing.

set -xv

trap 'exit' ERR

source /etc/profile.d/modules.sh
module use $HOME/modules/odysseus
module purge
module load qchem/gatekeeper

cd $QCAUX

svn update .

cd $QCREF

# We don't checkout the 'trunk' branch here, because we only cloned
# the SVN trunk, not the whole tree.
git checkout master
git svn fetch
git svn rebase
