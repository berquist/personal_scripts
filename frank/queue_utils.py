#!/usr/bin/env python

from __future__ import print_function

import subprocess as sp

import re
re_ints = re.compile('\d*')


def getargs():

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-u',
                        dest='username',
                        nargs='+',
                        help="""""")

    parser.add_argument('--debug',
                        action='store_true',
                        help="""""")

    args = parser.parse_args()

    return args


def make_spaced_dashes(lints):
    return ' '.join([('-' * lint) for lint in lints])


def parse_qstat_full_output(full_output, debug=False):

    jobinfo = dict()

    for full_output_line in full_output.splitlines():

        chomp = full_output_line.split()

        if len(chomp) > 2:
            key = chomp[0]
            value = ' '.join(chomp[2:])
            jobinfo[key] = value
        else:
            oldvalue = jobinfo[key]
            newvalue = ''.join([oldvalue, full_output_line])
            jobinfo[key] = newvalue.replace('\t', '')

    if debug:
        print(jobinfo)

    return jobinfo


def get_qstat_short_output(usernames=None, ids=None):

    if usernames:
        if len(usernames) == 1:
            # This will capture both a single usename and the typical
            # comma-separated list without spaces.
            qstat_cmd = ['qstat', '-u', usernames[0]]
        else:
            qstat_cmd = ['qstat', '-u', ','.join(usernames)]
    # usernames are taking precedence over job ids
    elif ids:
        qstat_cmd = ['qstat', '-a', ' '.join(ids)]
    else:
        qstat_cmd = ['qstat', '-a']

    short_output = sp.check_output(qstat_cmd).decode('utf-8').splitlines()
    short_output = short_output[5:]

    return short_output


def get_qstat_full_outputs(short_output):

    full_outputs = []

    for idx, short_output_line in enumerate(short_output):

        short_output_line_chomp = short_output_line.split()
        job = re_ints.match(short_output_line_chomp[0])
        jobid = job.group()

        try:
            full_output = sp.check_output(['qstat', '-f', str(jobid)]).decode('utf-8')
            full_outputs.append(full_output)
        except sp.CalledProcessError as e:
            continue

    return full_outputs
