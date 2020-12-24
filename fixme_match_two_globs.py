#!/usr/bin/env python

"""match_two_globs.py: Given two shell globs that each return a set of
filesystem matches, determine which results don't have matches
(excluding the differences between the glob expressions), and print
the result.
"""


import argparse
import os
import glob


parser = argparse.ArgumentParser()
parser.add_argument('glob1')
parser.add_argument('glob2')
args = parser.parse_args()

glob1_rep = args.glob1.replace('*', '')
glob2_rep = args.glob2.replace('*', '')

glob1_res = glob.glob(args.glob1)
glob2_res = glob.glob(args.glob2)

for idx1, res1 in enumerate(glob1_res):
    if res1.replace

for idx2, res2 in enumerate(glob2_res):
    for res1 in glob1_res:
        pass
