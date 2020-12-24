#!/usr/bin/env python

"""qfilter.py: For displaying all jobs in the queue except for jobs
belonging to the given user(s).
"""


import argparse
import subprocess as sp


parser = argparse.ArgumentParser()

parser.add_argument('user', nargs='+')

args = parser.parse_args()

stream = sp.check_output(['qstat', '-a']).decode('utf-8')
job_lines = [line for line in stream.split('\n')
             if not any(user in line for user in args.user)]
for line in job_lines:
    print(line)
