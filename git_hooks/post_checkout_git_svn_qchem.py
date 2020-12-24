#!/usr/bin/env python

# post_checkout_git_svn_qchem.py: For Q-Chem git-svn repositories,
# check out SVN externals and keep them up to date.

# Add as "post-checkout" under ${GIT_DIR}/.git/hooks.

# Modified from http://stackoverflow.com/a/8040405/3249688 then ported
# to Python.


import os
import re
import shutil
import subprocess as sp

ENCODING = "utf-8"


def rm_r(path):
    if not os.path.exists(path):
        return
    if os.path.isfile(path) or os.path.islink(path):
        os.unlink(path)
    else:
        shutil.rmtree(path)


if __name__ == '__main__':

    info = sp.check_output("git svn info".split()).decode(ENCODING)
    revision = re.search("Revision: ([1-9][0-9]*)", info).groups()[0]
    parent_url = "https://jubilee.q-chem.com"

    externals = sp.check_output("git svn -r{revision} propget svn:externals".format(**globals()).split()).decode(ENCODING)

    for external in externals.splitlines():
        checkout_args = external.split()
        if checkout_args:
            assert len(checkout_args) == 3
            checkout_rev = re.search("([1-9][0-9]*)", checkout_args[0]).groups()[0]
            checkout_url = parent_url + checkout_args[1]
            checkout_dirname = checkout_args[2]
            print(checkout_rev, checkout_url, checkout_dirname)
            checkout_cmd = "svn checkout -r{checkout_rev} {checkout_url} {checkout_dirname}".format(**locals()).split()
            try:
                checkout_output = sp.check_output(checkout_cmd).decode(ENCODING)
            except sp.CalledProcessError:
                # This happens when changing to a new SVN tag. Wipe the directory and try again.
                print(checkout_output)
                rm_r(checkout_dirname)
                try:
                    checkout_output = sp.check_output(checkout_cmd).decode(ENCODING)
                except sp.CalledProcessError:
                    print(checkout_output)
                    print("Failed again? Giving up...")
                    raise


    # git svn -r${revision} propget svn:externals | head -n-1 | {
    #     while read -r checkout_args
    #     do

    #         # Assume that each line has 3 components: revision number,
    #         # "url", and result directory.
    #         checkout_rev=$(echo ${checkout_args} | cut -d' ' -f1)
    #         checkout_url="${parent_url}$(echo ${checkout_args} | cut -d' ' -f2)"
    #         checkout_dirname=$(echo ${checkout_args} | cut -d' ' -f3)

    #         echo ${checkout_rev} ${checkout_url} ${checkout_dirname}
    #         svn checkout ${checkout_rev} ${checkout_url} ${checkout_dirname}
    #         if [ -z $(grep ${checkout_dirname} .git/info/exclude) ]
    #         then
    #             echo ${checkout_dirname} >> .git/info/exclude
    #         fi

    #     done
    # }
