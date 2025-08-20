#!/usr/bin/env bash

# TODO find the StackOverflow link this was adapted from

# TOOD generalize beyond Q-Chem ($QCSVN)

set -euo pipefail

# This grabs a clean list of branches. I remove formatting spaces at the
# beginning of each line, and I'm ignoring tags for now:
git branch -r | sed 's|^[[:space:]]*||' | grep -v '^tags/' > git-branch-list

# I grab a similar list of branches from svn, again removing formatting
# and trailing forward-slashes:
svn ls $QCSVN/branches | sed 's|^[[:space:]]*||' | sed 's|/$||' > svn-branch-list

# I diff the lists, find the lines that don't exist in the svn list anymore,
# remove the diff formatting, get rid of the "trunk" branch (which is a
# git-svn convenience) and save the results to a new list:
diff -u git-branch-list svn-branch-list | grep '^-' | sed 's|^-||' | grep -v '^trunk$' | grep -v '^--' > old-branch-list

# Now I just perform standard branch removal procedures for git-svn:
for i in $(cat old-branch-list); do
    git branch -d -r "$i"
    rm -rf .git/svn/refs/remotes/"$i"
done
