#!/usr/bin/env python

"""qfilter.py: For displaying all jobs in the queue except for the given user's jobs.
"""

from __future__ import print_function

import argparse
import subprocess as sp


parser = argparse.ArgumentParser()
parser.add_argument('user', type=str)
args = parser.parse_args()

stream = sp.check_output(['qstat', '-a']).decode('utf-8')
job_lines = [line for line in stream.split('\n') if line.find(args.user) == -1]
for line in job_lines:
    print(line)
