#!/usr/bin/env bash

# qchem_01_git_rebase_from_qchem_trac_trunk.sh
# Run this script (usually via cron) to load the git-svn Q-Chem repository
# (the "gatekeeper" repository) and update it from Q-Chem HQ's trunk
# via `git svn rebase`.

set -xv

trap 'exit' ERR

source /etc/profile.d/modules.sh
module use $HOME/modules/odysseus
module purge
module load qchem/gatekeeper

cd $QC

# Update the gatekeeper's copy of the trunk.
git checkout trunk
git svn fetch
git svn rebase
