#!/usr/bin/env python2

"""
qfilter.py

For displaying all jobs in the queue except for the given user's jobs.
"""

import os
import re
import subprocess as sp

stream = sp.check_output(["qstat", "-a"])
job_lines = [line for line in stream.split('\n') if line.find("vriesjk") == -1]
for line in job_lines:
    print line

