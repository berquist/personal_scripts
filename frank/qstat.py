#!/usr/bin/env python

from __future__ import print_function

import sys

from queue_utils import getargs
from queue_utils import make_spaced_dashes
from queue_utils import get_qstat_short_output
from queue_utils import get_qstat_full_outputs
from queue_utils import parse_qstat_full_output


if __name__ == '__main__':

    args = getargs()
    usernames = args.username

    blank_spot = '--'

    reformatted_lines = []

    short_output = get_qstat_short_output(usernames)
    full_outputs = get_qstat_full_outputs(short_output)

    for full_output in full_outputs:

        jobinfo = parse_qstat_full_output(full_output, debug=args.debug)

        jobid = jobinfo['Job'].split('.')[0]
        username = jobinfo['euser']
        group = jobinfo['egroup']
        queue = jobinfo['queue']
        jobname = jobinfo['Job_Name']
        session_id = jobinfo.get('session_id', blank_spot)
        nodes = jobinfo['Resource_List.nodect']
        # tasks = short_output_line_chomp[6]
        tasks = jobinfo['Resource_List.nodes'].split('=')[-1]
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
