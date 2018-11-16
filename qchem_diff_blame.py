#!/usr/bin/env python

'''
qchem.diff_blame.py: Given two Q-Chem Git repositories, compate the results
of `git blame` on every single file.
'''

import os
import filecmp
import subprocess as sp
import difflib


def blame_tree(dir1, dir2):
    dcmp = filecmp.dircmp(dir1, dir2, ignore=['.svn', '.git'])

    dcmp.common_files.sort()
    for common_file in dcmp.common_files:
        print(os.path.join(dir1, common_file))

        os.chdir(dir1)
        try:
            blame1 = sp.check_output(' '.join(['git', 'blame',
                                               os.path.join(dir1, common_file)]),
                                     shell=True).decode().splitlines()
        except sp.CalledProcessError as e:
            blame1 = e.output.decode().splitlines()

        os.chdir(dir2)
        try:
            blame2 = sp.check_output(' '.join(['git', 'blame',
                                               os.path.join(dir2, common_file)]),
                                     shell=True).decode().splitlines()
        except sp.CalledProcessError as e:
            blame2 = e.output.decode().splitlines()

        print('=' * 78)
        for line in difflib.unified_diff(blame1, blame2):
            print(line)
        print('=' * 78)

    dcmp.common_dirs.sort()
    for common_dir in dcmp.common_dirs:
        blame_tree(os.path.join(dir1, common_dir),
                   os.path.join(dir2, common_dir))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('dir1')
    parser.add_argument('dir2')
    args = parser.parse_args()

    blame_tree(args.dir1, args.dir2)
