#!/usr/bin/env python

import argparse
import subprocess as sp
import os
import socket
import shutil

parser_description = '''Compare Q-Chem test outputs with reference outputs.
$QC, $QCREF, and $QCPLATFORM must be defined.'''

parser = argparse.ArgumentParser(description=parser_description)
parser.add_argument('--copy', dest='copy', action='store_true',
                    help='''Copy the problem outputs to ~/qchem_test_outputs
                    with the appropriate hostname.''')
parser.add_argument('--delim', dest='delim', default=socket.gethostname(),
                    help='''The (hopefully) unique delimiter added for the
                    copied test outputs.''')
args = parser.parse_args()
copy = args.copy
delim = args.delim

os.chdir(os.path.expandvars('$QC/test'))

command1 = os.path.expandvars('csh -f $QC/test/tablecompare.csh')
tablecompare = subprocess.check_output(command1.split())

print(tablecompare)

command2_stub = os.path.expandvars('csh -f $QC/util/cronutil/monCompare.csh -v ')
output_path = os.path.expandvars('$HOME/qchem_test_outputs')

for line in tablecompare.splitlines():
    l = line.split()
    if l == []:
        continue
    elif l[0] == '[' and l[1][-4:] == '.out':
        command2 = command2_stub + l[1]
        # The monCompare script will return 1 if outputs differ; who cares,
        # we just want the output.
        try:
            diff = sp.check_output(command2.split()).decode()
        except sp.CalledProcessError as e:
            diff = e.output.decode()
        print('=' * 78)
        print('job:', l[1])
        print(diff)
        print('=' * 78)
        print('\n')
        if copy:
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            filename = os.path.splitext(l[1])[0] + '.' + delim + os.path.splitext(l[1])[1]
            shutil.copy2(l[1], output_path + '/' + filename)
