#!/usr/bin/env python

'''

Usage:
  orca.mrci_analysis.py [options] <outputfilename>

Options:
  --print_args  Print the argument block.
'''

from __future__ import print_function


def parse_absorption_spectrum(outputfile):
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
    line = next(outputfile)
    while 'g-factors' not in line:
        line = next(outputfile)
    line = next(outputfile)
    g_xx, g_yy, g_zz = list(map(float, line.split()[:3]))
    g_perp = (g_xx + g_yy) / 2
    g_para = g_zz
    print(' g_perp: {}'.format(g_perp))
    print(' g_para: {}'.format(g_para))


def parse_state_block_cas(outputfile):
    roots = []
    configurations = []
    next(outputfile)
    next(outputfile)
    line = next(outputfile)
    t_root_g = 'ROOT {}: E= {} Eh'
    t_root_e = 'ROOT {}: E= {} Eh {} eV {} cm**-1'
    while line.split() != []:
        root = dict()
        if 'ROOT' in line:
            root['configurations'] = configurations
            roots.append(root)
            configurations = []
            root = dict()
            root['num'] = int(line.split()[1][:-1])
            root['energy_hartree'] = float(line.split()[3])
            # If not the ground state, parse excitation energies too.
            if root['num'] > 0:
                root['energy_ev'] = float(line.split()[5])
                root['energy_wavenumber'] = float(line.split()[7])
            line = next(outputfile)
        # coeff = float(line.split()[0])
        # hole_idx = int(line.split()[2][:-2])
        # occ = line.split()[-1]
        # configuration = (coeff, hole_idx, occ)
        # configurations.append(configuration)
        # line = next(outputfile)
    for root in roots:
        print(root)
        # if root['num'] == 0:
        #     print(t_root_g.format(root['num'],
        #                           root['energy_hartree']))
        # else:
        #     print(t_root_e.format(root['num'],
        #                           root['energy_hartree'],
        #                           root['energy_ev'],
        #                           root['energy_wavenumber']))


def parse_state_block_ci(outputfile):
    line = next(outputfile)
    while 'STATE' not in line:
        line = next(outputfile)
    states = []
    while '------------------------------' not in line:
        if 'STATE' in line:
            state = dict()
            state['num'] = int(line.split()[1][:-1])
            state['refweight'] = float(line.split()[6])
            state['energy_hartree'] = float(line.split()[3])
            state['energy_ev'] = float(line.split()[7])
            state['energy_wavenumber'] = float(line.split()[9])
            states.append(state)
            line = next(outputfile)
    print(states)

if __name__ == '__main__':

    from docopt import docopt
    import os.path

    args = docopt(__doc__)

    if args['--print_args']:
        print(args)

    outputfilename = args['<outputfilename>']
    stub = os.path.splitext(outputfilename)[0]

    print('-' * 78)
    print(outputfilename)

    with open(outputfilename) as outputfile:
        for line in outputfile:
            # Parse the state blocks after CASSCF but before the MRCI.
            if 'CAS-SCF STATES FOR BLOCK' in line:
                print(line.strip())
                # parse_state_block_cas(outputfile)
            # Parse the state block after the MRCI.
            if 'CI-RESULTS' in line:
                print(line.strip())
                parse_state_block_ci(outputfile)
            # Parse the absorption spectrum block.
            if 'CI-EXCITATION SPECTRA' in line:
                print(line.strip(), '(no SOC correction)')
                parse_absorption_spectrum(outputfile)
            # Parse the g-tensor block.
            if 'ELECTRONIC G-MATRIX' in line:
                parse_g_tensor(outputfile)


    print('-' * 78)
