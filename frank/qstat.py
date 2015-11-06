#!/usr/bin/env python

from __future__ import print_function

import re
import subprocess as sp
import sys

from queue_utils import make_spaced_dashes


def getargs():

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-u',
                        dest='username',
                        nargs='+',
                        help="""""")

    args = parser.parse_args()

    return args



if __name__ == '__main__':

    args = getargs()
    usernames = args.username

    if usernames:
        if len(usernames) == 1:
            # This will capture both a single usename and the typical
            # comma-separated list without spaces.
            qstat_cmd = ['qstat', '-u', usernames[0]]
        else:
            qstat_cmd = ['qstat', '-u', ','.join(usernames)]
    else:
        qstat_cmd = ['qstat', '-a']

    short_output = sp.check_output(qstat_cmd).decode('utf-8').splitlines()
    short_output = short_output[5:]

    re_ints = re.compile('\d*')

    blank_spot = '--'

    reformatted_lines = []

    for idx, short_output_line in enumerate(short_output):

        jobinfo = dict()
        short_output_line_chomp = short_output_line.split()
        job = re_ints.match(short_output_line_chomp[0])
        jobid = job.group()

        try:
            full_output = sp.check_output(['qstat', '-f', str(jobid)]).decode('utf-8')
        except sp.CalledProcessError as e:
            continue

        for full_output_line in full_output.splitlines():

            chomp = full_output_line.split()

            if 'Id:' in chomp:
                pass
            elif len(chomp) > 2:
                key = chomp[0]
                value = ' '.join(chomp[2:])
                jobinfo[key] = value
            else:
                oldvalue = jobinfo[key]
                newvalue = ''.join([full_output_line, oldvalue])
                jobinfo[key] = newvalue

        username = jobinfo['euser']
        group = jobinfo['egroup']
        queue = jobinfo['queue']
        jobname = jobinfo['Job_Name']
        session_id = jobinfo.get('session_id', blank_spot)
        # nodes = jobinfo['Resource_List.nodect']
        nodes = short_output_line_chomp[5]
        tasks = short_output_line_chomp[6]
        reqd_mem = jobinfo.get('Resource_List.pmem', blank_spot)
        reqd_time = jobinfo['Resource_List.walltime']
        status = jobinfo['job_state']
        elap_time = jobinfo.get('resources_used.walltime', blank_spot)

        reformatted_lines.append([
            jobid,
            username,
            group,
            queue,
            jobname,
            session_id,
            nodes,
            tasks,
            reqd_time,
            elap_time,
            status
        ])

    # If there aren't any results, terminate gracefully.
    if len(reformatted_lines) == 0:
        sys.exit(0)

    max_len_jobid = max(len(l[0]) for l in reformatted_lines)
    max_len_username = max(max(len(l[1]) for l in reformatted_lines), len('Username'))
    max_len_group = max(max(len(l[2]) for l in reformatted_lines), len('Group'))
    max_len_queue = max(max(len(l[3]) for l in reformatted_lines), len('Queue'))
    max_len_jobname = max(max(len(l[4]) for l in reformatted_lines), len('Jobname'))
    max_len_session_id = max(max(len(l[5]) for l in reformatted_lines), len('SID'))
    max_len_nodes = max(max(len(l[6]) for l in reformatted_lines), len('Nodes'))
    max_len_tasks = max(max(len(l[7]) for l in reformatted_lines), len('Cores'))
    max_len_reqd_time = max(max(len(l[8]) for l in reformatted_lines), len('Time (R)'))
    max_len_elap_time = max(max(len(l[9]) for l in reformatted_lines), len('Time (E)'))
    max_len_status = max(max(len(l[10]) for l in reformatted_lines), len('S'))

    rlt = '{{:{}}} {{:{}}} {{:{}}} {{:{}}} {{:{}}} {{:>{}}} {{:>{}}} {{:>{}}} {{:>{}}} {{:>{}}} {{:{}}}'.format(
        max_len_jobid,
        max_len_username,
        max_len_group,
        max_len_queue,
        max_len_jobname,
        max_len_session_id,
        max_len_nodes,
        max_len_tasks,
        max_len_reqd_time,
        max_len_elap_time,
        max_len_status
    )
    print(rlt.format(
        'ID',
        'Username',
        'Group',
        'Queue',
        'Jobname',
        'SID',
        'Nodes',
        'Cores',
        'Time (R)',
        'Time (E)',
        'S'
    ))
    print(make_spaced_dashes([
        max_len_jobid,
        max_len_username,
        max_len_group,
        max_len_queue,
        max_len_jobname,
        max_len_session_id,
        max_len_nodes,
        max_len_tasks,
        max_len_reqd_time,
        max_len_elap_time,
        max_len_status
]))

    for reformatted_line in reformatted_lines:
        print(rlt.format(*reformatted_line))
