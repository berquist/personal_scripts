#!/usr/bin/env python

'''Extract all information from an anharmonic frequency calculation.

Each vibrational mode is a dictionary whose keys represent the level of
theory for which a result exists (harmonic, TOSH, VPT2, VCI). The number
associated with any VCI entry refers to the number of quanta.

Usage:
  qchem_vci_analysis.py [options] <outputfilename>

Options:
  --print_dict  Print the parsed dictionary.
  --print_args  Print the argument block.
'''

from __future__ import print_function

from collections import OrderedDict
from itertools import count

from docopt import docopt
from cclib.io import ccopen


def parse_vibrational_anharmonic_analysis(outputfilename):
    cclib_job = ccopen(outputfilename)
    cclib_data = cclib_job.parse()

    # If we can't even find harmonic frequencies, jump out here.
    try:
        nmodes = len(cclib_data.vibfreqs)
    except:
        return dict()

    mode_dict = dict()
    for mode in range(1, nmodes + 1):
        mode_dict[mode] = OrderedDict()

    for mode, harmonic_frequency in zip(count(start=1), cclib_data.vibfreqs):
        mode_dict[mode]['harmonic'] = harmonic_frequency

    with open(outputfilename) as outputfile:
        line = ''
        while 'VIBRATIONAL ANHARMONIC ANALYSIS' not in line:
            try:
                line = next(outputfile)
            # We only need one try/except, since if we don't match here,
            # we'll never match.
            except StopIteration:
                return mode_dict
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
                # quanta = float(line.split()[-4])
                freq = float(line.split()[-1])
                mode_dict[mode][key] = freq
                line = next(outputfile)
            else:
                line = next(outputfile)

    return mode_dict


def main(args=None, outputfilename=None):
    if args['--print_args']:
        print(args)

    outputfilename = args['<outputfilename>']

    mode_dict = parse_vibrational_anharmonic_analysis(outputfilename)

    return mode_dict


if __name__ == '__main__':

    args = docopt(__doc__)

    mode_dict = main(args=args)

    if args['--print_dict']:
        try:
            for mode in mode_dict:
                print('Mode {}:'.format(mode))
                for calculation_type in mode_dict[mode]:
                    print(' {:10}: {}'.format(calculation_type,
                                              mode_dict[mode][calculation_type]))
        except:
            print('No frequencies present.')
