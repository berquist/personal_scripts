#!/usr/bin/env python

'''

Usage:
  orca_mrci_analysis.py [options] <outputfilename>

Options:
  --cutoff_weight=CWEIGHT  Cutoff weight for printing a configuration. [Default: 0.5]
  --print_args             Print the argument block.
'''

from __future__ import print_function

from docopt import docopt
import os.path
import re


t_root_g = ' ROOT {}: E= {:.8f} Eh'
t_root_e = ' ROOT {}: E= {:.8f} Eh {:.2f} eV {:.1f} cm**-1'
t_root = ' ROOT {}: E= {:.8f} Eh {:.2f} eV {:.1f} cm**-1'
t_config = '  {:.4f} [{}]'


def parse_absorption_spectrum(outputfile):
    """Parse an absorption spectrum block, printing it to stdout.
    """
    line = next(outputfile)
    while 'ABSORPTION SPECTRUM' not in line:
        line = next(outputfile)
    next(outputfile)
    next(outputfile)
    next(outputfile)
    next(outputfile)
    line = next(outputfile)
    print('state from state to       cm-1      eV')
    t = '{:10} {:8} {:10.1f} {:7.3f}'
    while line.split() != []:
        state_from = int(line[0:3])
        state_to = int(line[9:11])
        energy_wavenumber = float(line.split()[-7])
        energy_ev = energy_wavenumber * 1.239842e-4
        print(t.format(state_from, state_to, energy_wavenumber, energy_ev))
        line = next(outputfile)


def parse_g_tensor(outputfile):
    """Parse the g-tensor block, printing the principal values to stdout.
    """
    line = next(outputfile)
    while 'g-factors' not in line:
        line = next(outputfile)
    line = next(outputfile)
    g_1, g_2, g_3 = list(map(float, line.split()[:3]))
    g_perp = (g_1 + g_2) / 2
    g_para = g_3
    print(' g_1: {} g_2: {} g_3: {}'.format(g_1, g_2, g_3))
    print(' g_perp: {}'.format(g_perp))
    print(' g_para: {}'.format(g_para))


def parse_state_block_cas(outputfile, cutoff_weight):
    """Parse an entire MCSCF state block, printing it to
    stdout.

    The sum of the coefficients == 1.
    """
    next(outputfile)
    next(outputfile)
    line = next(outputfile)
    roots = []
    root = dict()
    configurations = []
    while line.strip().split() != []:
        if 'ROOT' in line:
            root['configurations'] = configurations
            roots.append(root)
            root = dict()
            configurations = []
            root['num'] = int(line.split()[1][:-1])
            root['energy_hartree'] = float(line.split()[3])
            # If not the ground state, parse excitation energies too.
            if root['num'] > 0:
                root['energy_ev'] = float(line.split()[5])
                root['energy_wavenumber'] = float(line.split()[7])
        else:
            coeff = float(line.split()[0])
            occ = line.split()[-1]
            configuration = (coeff, occ)
            configurations.append(configuration)
        line = next(outputfile)
    del roots[0]
    root['configurations'] = configurations
    roots.append(root)
    for root in roots:
        if root['num'] == 0:
            print(t_root_g.format(root['num'],
                                  root['energy_hartree']))
        else:
            print(t_root_e.format(root['num'],
                                  root['energy_hartree'],
                                  root['energy_ev'],
                                  root['energy_wavenumber']))
        for configuration in root['configurations']:
            if configuration[0] > cutoff_weight:
                print(t_config.format(*configuration))


def parse_state_block_ci(outputfile, cutoff_weight):
    """Parse an entire MRCI state block, printing it to
    stdout.
    """
    line = next(outputfile)
    while 'STATE' not in line:
        line = next(outputfile)
    roots = []
    root = dict()
    configurations = []
    while line.strip().split() != []:
        if 'STATE' in line:
            root['configurations'] = configurations
            roots.append(root)
            root = dict()
            configurations = []
            root['num'] = int(line.split()[1][:-1])
            root['refweight'] = float(line.split()[6])
            root['energy_hartree'] = float(line.split()[3])
            root['energy_ev'] = float(line.split()[7])
            root['energy_wavenumber'] = float(line.split()[9])
        else:
            coeff = float(line.split()[0])
            occ = re.search('\[(0|1|2)+\]', line).group()[1:-1]
            configuration = (coeff, occ)
            configurations.append(configuration)
        line = next(outputfile)
    del roots[0]
    root['configurations'] = configurations
    roots.append(root)
    for root in roots:
        print(t_root.format(root['num'],
                            root['energy_hartree'],
                            root['energy_ev'],
                            root['energy_wavenumber']))
        for configuration in root['configurations']:
            if configuration[0] > cutoff_weight:
                print(t_config.format(*configuration))


def main(args):
    outputfilename = args['<outputfilename>']
    stub = os.path.splitext(outputfilename)[0]

    cutoff_weight = float(args['--cutoff_weight'])
    print('Using a cutoff weight of {}'.format(cutoff_weight))

    print('-' * 78)
    print(outputfilename)

    with open(outputfilename) as outputfile:
        for line in outputfile:
            # Parse the state blocks after CASSCF but before the MRCI.
            if 'CAS-SCF STATES FOR BLOCK' in line:
                print(line.strip())
                parse_state_block_cas(outputfile, cutoff_weight)
            # Parse the state block(s) after the MRCI. There might be
            # more than one, especially if doing SORCI/SORCP (which
            # are two-step jobs).
            if 'CI-RESULTS' in line:
                print(line.strip())
                parse_state_block_ci(outputfile, cutoff_weight)
            # Parse the absorption spectrum block.
            if 'CI-EXCITATION SPECTRA' in line:
                print(line.strip(), '(no SOC correction)')
                parse_absorption_spectrum(outputfile)
            # Parse the g-tensor block.
            if 'ELECTRONIC G-MATRIX' in line:
                parse_g_tensor(outputfile)

    print('-' * 78)


if __name__ == '__main__':

    args = docopt(__doc__)

    if args['--print_args']:
        print(args)

    main(args)
