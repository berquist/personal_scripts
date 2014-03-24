#!/usr/bin/env python

import argparse
import os
import os.path
# import glob
import filecmp
import subprocess

"""
qchem.diff_tests.py: Given two test directories with output files, perform a
raw UNIX diff between matching files.
"""

parser = argparse.ArgumentParser()
parser.add_argument("dir1")
parser.add_argument("dir2")
args = parser.parse_args()
dir1 = args.dir1
dir2 = args.dir2

# outputs1 = glob.glob(dir1 + "/*.out")
# outputs2 = glob.glob(dir2 + "/*.out")

# Now we need to match the proper pairs. If there are excess files,
# exclude them.

dcmp = filecmp.dircmp(dir1, dir2)
outputs = [f for f in dcmp.common_files if f[-4:] == ".out"]
outputs.sort()

for f in outputs:
    print "================================================================================"
    print "job: {}".format(f)
    subprocess.call(["diff", os.path.join(dir1, f), os.path.join(dir2, f)])
    print "================================================================================"
