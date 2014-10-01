#!/usr/bin/env python2

import argparse
import re
import subprocess as sp

parser = argparse.ArgumentParser(description='Drink Coffee: Do Stupid Things Faster With More Energy')
parser.add_argument('-u', dest='username', type=str, metavar='<username>', help='')
args = parser.parse_args()
username = args.username

# get all the user's jobs in short format and discard the first 5 lines
short_output = sp.check_output('qstat -u {}'.format(username).split()).splitlines()
header = short_output[:5]
short_output = short_output[5:]

regex = re.compile('\d*') # return all integers
for idx, line in enumerate(short_output):
    job = regex.match(line.strip().split()[0])
    jobid = job.group()
    full_output = sp.check_output(['qstat', '-f', str(jobid)])

    # get the full job name and queue from the full output
    tmp = full_output.splitlines()
    jobname = tmp[1].split()[2]
    queue = tmp[8].split()[2]

    short_output[2] = queue
    short_output[3] = jobname
    print short_output
