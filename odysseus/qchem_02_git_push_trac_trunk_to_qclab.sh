#!/usr/bin/env bash

# qchem_02_git_push_trac_trunk_to_qclab.sh
# Run this script (usually via cron) to load the git-svn Q-Chem repository
# (the "gatekeeper" repository) and push its (updated) trunk to our group's
# "working" git repository (called "qclab", stored in
# `/home/git/github/qchem.git`).

trap 'exit' ERR

source /etc/profile.d/modules.sh
module use $HOME/modules/odysseus
module purge
module load qchem/gatekeeper

cd $QC

git checkout trunk
git push qclab trunk
