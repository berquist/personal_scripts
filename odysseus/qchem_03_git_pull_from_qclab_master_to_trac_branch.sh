#!/usr/bin/env bash

# qchem_03_git_pull_from_qclab_master_to_trac_branch.sh
# Run this script (manually) to load the git-svn Q-Chem repository
# (the "gatekeeper" repository) [...]

set -xv

trap 'exit' ERR

source /etc/profile.d/modules.sh
module use $HOME/modules/odysseus
module purge
module load qchem/gatekeeper

branchname=lambrechtlab

cd $QC
git checkout trunk
git svn fetch
git svn rebase

# Delete the branch at HQ:
svn rm -m "Deleting before push." $QCSVN/branches/$branchname
# Delete the branch locally:
git branch -D -r $branchname
# The second 'svn' appears because we cloned with `--prefix=svn/`.
# Would this be different if we used git svn clone --std-layout?
rm -rf ./.git/svn/refs/remotes/svn/$branchname

# Make a clean local copy of the branch:
git checkout -B $branchname --no-track
# Pull from qclab/master:
git pull --rebase qclab master:lambrechtlab

# This will create the SVN branch.
# The `-n` is for `--dry-run`. Remove to actually create the branch.
git svn branch -n -m "Enter a sensible branch creation message here." $branchname
# git svn branch $branchname


git rebase svn/$branchname
git svn dcommit -n
# git svn dcommit
