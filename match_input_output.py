#!/usr/bin/env python

"""match_input_output.py: Given input and output file extensions, determine
which ones don't have matching partners (in the current directory),
and print the result.
"""

from __future__ import print_function

import argparse
import os
import glob


# pylint: disable=C0103
parser = argparse.ArgumentParser()
parser.add_argument('ext_inp', help='the extension for input files')
parser.add_argument('ext_out', help='the extension for output files')
args = parser.parse_args()
ext_inp = args.ext_inp
ext_out = args.ext_out

# Get the results from `ls`:
directory = os.getcwd()
inputs = [os.path.basename(f) for f in glob.glob(directory + '/*.' + ext_inp)]
outputs = [os.path.basename(f) for f in glob.glob(directory + '/*.' + ext_out)]

# How should we compare the elements in each?
# Turn everything into stubs (no extensions):
inputs_stubs = [os.path.splitext(f)[0] for f in inputs]
outputs_stubs = [os.path.splitext(f)[0] for f in outputs]

# Loop through each list of stubs separately.
for iidx, istub in enumerate(inputs_stubs):
    if istub not in outputs_stubs:
        print(inputs[iidx])
for oidx, ostub in enumerate(outputs_stubs):
    if ostub not in inputs_stubs:
        print(outputs[oidx])
