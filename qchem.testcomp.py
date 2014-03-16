#!/usr/bin/env python

import argparse
import subprocess
import os.path
import os
import socket
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('--copy', action='store_true', help='Copy the problem outputs to ~/qchem_test_outputs with the appropriate hostname.')
args = parser.parse_args()
copy = args.copy

os.chdir(os.path.expandvars('$QC/test'))

command1 = os.path.expandvars('csh -f $QC/test/tablecompare.csh')
tablecompare = subprocess.check_output(command1.split())

print tablecompare

command2_stub = os.path.expandvars('csh -f $QC/util/cronutil/monCompare.csh -v ')
output_path = os.path.expandvars('$HOME/qchem_test_outputs')

for line in tablecompare.splitlines():
    l = line.split()
    if l == []:
        continue
    elif l[0] == '[' and l[1][-4:] == '.out':
        command2 = command2_stub + l[1]
        subprocess.call(command2.split())
        if copy:
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            filename = os.path.splitext(l[1])[0] + '.' + socket.gethostname() + os.path.splitext(l[1])[1]
            shutil.copy2(l[1], output_path + '/' + filename)
