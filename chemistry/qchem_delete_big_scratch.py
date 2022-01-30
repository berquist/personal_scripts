#!/usr/bin/env python

"""qchem_delete_big_scratch.py: Delete 'big' scratch files created by
Q-Chem that we probably won't ever want to read from."""


import argparse
import glob
import os
import os.path

# Each file has a glob at the end because each MPI process creates its
# own copy; make sure we get them all.
SCRATCHFILES = (
    '48.*', # GRID
    '49.*', # INTERP_TABLE
    '181.*' # GRID_DERIV
)

parser = argparse.ArgumentParser()
parser.add_argument(
    "scratchdir", nargs="?", default=".", help="path to the top-level scratch directory"
)
args = parser.parse_args()
scratchdir = args.scratchdir

for (dirpath, dirnames, filenames) in os.walk(scratchdir):
    for scratchfile in SCRATCHFILES:
        results = glob.glob(os.path.join(dirpath, scratchfile))
        for result in results:
            try:
                os.remove(result)
                print("Removed {}".format(result))
            except:
                print("Couldn't remove {}".format(result))
