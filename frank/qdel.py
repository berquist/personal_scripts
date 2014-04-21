#!/usr/bin/env python2

"""qdel.py: For deleting all PBS jobs within a given set of ids (including those)."""

import argparse
import subprocess as sp

parser = argparse.ArgumentParser(description='Drink Coffee: Do Stupid Things Faster With More Energy')
parser.add_argument('start')
parser.add_argument('end')
args = parser.parse_args()
start = int(args.start)
end = int(args.end)

for jobid in range(start, end+1):
    sp.call("qdel {}".format(jobid), shell=True)

