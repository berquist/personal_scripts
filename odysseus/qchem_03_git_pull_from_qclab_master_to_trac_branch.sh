#!/usr/bin/env bash

# qchem_03_git_pull_from_qclab_master_to_trac_branch.sh
# Run this script (manually) to load the git-svn Q-Chem repository
# (the "gatekeeper" repository) [...]

trap 'exit' ERR

source /etc/profile.d/modules.sh
module use $HOME/modules/odysseus
module purge
module load qchem/gatekeeper

cd $QC

# Delete the branch at HQ:
svn rm  -m "Deleting before push." $QCSVN/branches/lambrecht
# Delete the branch locally:
git branch -D -r lambrecht
# The second 'svn' appears because we cloned with `--prefix=svn/`.
rm -rf ./.git/svn/refs/remotes/svn/lambrecht

# Make a clean local copy of the branch:
git checkout -B lambrecht --no-track
# Pull from qclab/master:
git pull qclab master

# This will create the SVN branch.
# The `-n` is for `--dry-run`. Remove to actually create the branch.
git svn branch -n -m "Enter a sensible branch creation message here." lambrecht
