#!/usr/bin/env python

"""calculate_rmsd_all.py: Call the `calculate_rmsd` Python script on
every possible pair of XYZ files in the current working directory.
"""


import subprocess as sp
from glob import glob

# pylint: disable=C0103
xyzfilenames = glob("*.xyz")
print(xyzfilenames)

for i in range(len(xyzfilenames)):
    for j in range(i):
        if i != j:
            fname1 = xyzfilenames[i]
            fname2 = xyzfilenames[j]
            print("file 1: {}".format(fname1))
            print("file 2: {}".format(fname2))
            # shell out, because `rmsd` may not be in PYTHONPATH for
            # import
            sp.call(["calculate_rmsd.py", fname1, fname2])
            print("=" * 78)
