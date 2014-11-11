#!/usr/bin/env python

'''

Usage:
  qchem_vci_analysis.py [options] <outputfilename>

Options:
  --print_args
'''

from __future__ import print_function

from docopt import docopt
import os.path
from cclib.parser import ccopen


def parse_vibrational_anharmonic_analysis(outputfile, nmodes):
    mode_dict = dict()
    for mode in range(1, nmodes + 1):
        mode_dict[mode] = dict()

    line = ''
    while 'VIBRATIONAL ANHARMONIC ANALYSIS' not in line:
        line = next(outputfile)
    while 'TOSH' not in line:
        line = next(outputfile)

    while line.strip().split() != []:
        mode = int(line[6:8])
        mode_dict[mode]['tosh'] = float(line[9:22])
        mode_dict[mode]['vpt2'] = float(line[30:])
        line = next(outputfile)

    line = next(outputfile)
    while list(set(line.strip())) != ['=']:
        if line.strip().split() != []:
            quantum = line[5:7].strip()
            key = 'vci' + quantum
            mode = int(line[13:15])
            quanta = float(line.split()[-4])
            freq = float(line.split()[-1])
            mode_dict[mode][key] = freq
            line = next(outputfile)
        else:
            line = next(outputfile)

    return mode_dict


def main(args):
    if args['--print_args']:
        print(args)

    outputfilename = args['<outputfilename>']
    # stub = os.path.splitext(outputfilename)[0]

    cclib_job = ccopen(outputfilename)
    cclib_data = cclib_job.parse()
    nmodes = len(cclib_data.vibfreqs)

    with open(outputfilename) as outputfile:
        parse_vibrational_anharmonic_analysis(outputfile, nmodes)


if __name__ == '__main__':

    args = docopt(__doc__)

    main(args)
