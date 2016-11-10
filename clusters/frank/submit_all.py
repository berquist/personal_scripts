#!/usr/bin/env python

from __future__ import print_function

from glob import glob
import subprocess

command_python = "submit-qchem-batch.py --walltime 144 --queue dist_small --ppn 16 --ppj 8 --nodes 4 --batchname batch_2qm_{number} drop_{number}_2qm_*.in".format

command_qsub = "qsub batch_2qm_{number}.pbs".format

inputfilenames = glob("drop_*_2qm_*.in")

numbers = list(set(int(ifname.split("_")[1])
                   for ifname in inputfilenames))

print(numbers)
print(len(numbers))

for number in numbers:
    cmd_p = command_python(number=number)
    cmd_q = command_qsub(number=number)
    print(cmd_p)
    subprocess.check_call(cmd_p, shell=True)
    # print(cmd_q)
    # subprocess.check_call(cmd_q, shell=True)
