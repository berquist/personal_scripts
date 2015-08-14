#!/usr/bin/env python

from glob import glob
import shutil

inputfiles = glob("drop*.in")

snapshot_numbers = []

for inputfile in inputfiles:
    split = inputfile.split('_')
    snapshot_numbers.append(int(split[1]))

snapshot_numbers = list(set(snapshot_numbers))

n_mm_pairs = (16, 32, 64, 128, 253, 254, 255, 256)

t = "drop_{}_2qm_{}mm.in".format
for snapshot_number in snapshot_numbers:
    for n_mm in n_mm_pairs:
        fn = t(snapshot_number, n_mm)
        try:
            shutil.copy2("../unused/{}".format(fn), '.')
            print(fn)
        except:
            print("Couldn't copy over {}".format(fn))
