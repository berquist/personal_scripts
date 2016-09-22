#!/bin/bash

# post_checkout_git_svn_qchem.bash: For Q-Chem git-svn repositories,
# check out SVN externals and keep them up to date.

# Add as "post-checkout" under ${GIT_DIR}/.git/hooks.

# Modified from http://stackoverflow.com/a/8040405/3249688

set -eu

revision=$(git svn info | sed -n 's/^Revision: \([1-9][0-9]*\)$/\1/p')
parent_url="https://jubilee.q-chem.com/"

git svn -r${revision} propget svn:externals | head -n-1 | {
    while read -r checkout_args
    do

        # Assume that each line has 3 components: revision number,
        # "url", and result directory.
        checkout_rev=$(echo ${checkout_args} | cut -d' ' -f1)
        checkout_url="${parent_url}$(echo ${checkout_args} | cut -d' ' -f2)"
        checkout_dirname=$(echo ${checkout_args} | cut -d' ' -f3)

        echo ${checkout_rev} ${checkout_url} ${checkout_dirname}
        svn checkout ${checkout_rev} ${checkout_url} ${checkout_dirname}
        if [ -z $(grep ${checkout_dirname} .git/info/exclude) ]
        then
            echo ${checkout_dirname} >> .git/info/exclude
        fi

    done
}
