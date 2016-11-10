#!/usr/bin/env python

from __future__ import print_function

import os.path

from queue_utils import getargs
from queue_utils import get_qstat_short_output
from queue_utils import get_qstat_full_outputs
from queue_utils import parse_qstat_full_output


if __name__ == '__main__':

    args = getargs()

    short_output = get_qstat_short_output(None, args.ids)
    full_outputs = get_qstat_full_outputs(short_output)
    jobinfos = [parse_qstat_full_output(full_output)
                for full_output in full_outputs]

    for jobinfo in jobinfos:
        assert 'Output_Path' in jobinfo.keys()
        output_path = os.path.dirname(jobinfo['Output_Path'].split(':')[1])
        print(output_path)
