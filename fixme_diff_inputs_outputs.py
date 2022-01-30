#!/usr/bin/env python

"""diff_inputs_outputs.py: ..."""

import argparse
import filecmp
import os.path
import subprocess as sp

parser = argparse.ArgumentParser()
parser.add_argument("dir1")
parser.add_argument("dir2")
args = parser.parse_args()
dir1 = args.dir1
dir2 = args.dir2

dcmp = filecmp.dircmp(dir1, dir2)
inputs = sorted([f for f in dcmp.common_files if os.path.splitext(f)[1] == "in"])
outputs = sorted([f for f in dcmp.common_files if os.path.splitext(f)[1] == "out"])
