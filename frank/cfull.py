#!/usr/bin/env python2

"""cfull.py: For displaying each of the given user's jobs in the full format
(like a combination of 'qstat -u <user>' and 'checkjob <job id>)"""

import os
import re
import argparse
import subprocess as sp

# signature:
# qfull.py -u <username>

parser = argparse.ArgumentParser(description='Drink Coffee: Do Stupid Things Faster With More Energy')
parser.add_argument('-u', dest='username', type=str, metavar='<username>', help='')
args = parser.parse_args()
username = args.username

# get all the user's jobs in short format
stream = os.popen('qstat -u {}'.format(username))

# discard the header information
for i in range(5):
    stream.readline()

regex = re.compile('\d*') # return all integers
jobs = stream.readlines() # list of job info strings
for line in jobs:
    job = regex.match(line.strip().split()[0])
    jobid = job.group()
    sp.call(['checkjob', str(jobid)])
