#!/usr/bin/env python

"""qchem_diff_tests.py: Given two test directories with output files,
perform a raw UNIX diff between matching files.
"""

import argparse
import os.path
import filecmp
import subprocess as sp


parser = argparse.ArgumentParser()
parser.add_argument('dir1')
parser.add_argument('dir2')
args = parser.parse_args()
dir1 = args.dir1
dir2 = args.dir2

# Now we need to match the proper pairs. If there are excess files,
# exclude them.

dcmp = filecmp.dircmp(dir1, dir2)
outputs = [f for f in dcmp.common_files if f[-4:] == '.out']
outputs.sort()

for f in outputs:
    print('=' * 78)
    print('========== job: {}'.format(f))
    try:
        diff = sp.check_output(['diff',
                                os.path.join(dir1, f),
                                os.path.join(dir2, f)]).decode()
    except sp.CalledProcessError as e:
        diff = e.output.decode()
    print(diff)
    print('=' * 78)
