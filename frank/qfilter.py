#!/usr/bin/env python

"""qfilter.py: For displaying all jobs in the queue except for the given user's jobs.
"""

from __future__ import print_function

import subprocess as sp


stream = sp.check_output(["qstat", "-a"])
job_lines = [line for line in stream.split('\n') if line.find("vriesjk") == -1]
for line in job_lines:
    print(line)
