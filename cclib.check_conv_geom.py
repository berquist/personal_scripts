#!/usr/bin/env python

'''cclib.check_conv_geom.py: Check if a geometry optimization job
has converged.'''

import argparse
from cclib.parser import ccopen

parser = argparse.ArgumentParser()
parser.add_argument('filenames', nargs = '+')
args = parser.parse_args()
filenames = args.filenames

def find_string_in_file(filename, string):
    with open(filename) as outputfile:
        for line in outputfile:
            if string in line:
                return True
    return False

for filename in filenames:

    job = ccopen(filename)
    # data = job.parse()

    if type(job) == 'cclib.parser.orcaparser.ORCA':
        string = 'THE OPTIMIZATION HAS CONVERGED'
    elif type(job) == 'cclib.parser.qchemparser.QChem':
        string = ''
    else:
        string = ''

    converged = find_string_in_file(filename, string)

    print('{}: {}'.format(filename, converged))
