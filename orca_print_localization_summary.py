#!/usr/bin/env python

'''

Usage:
  orca_print_localization_summary.py [options] <outputfilename>

Options:
  --only-bond-like  Only print the bond-like localized MOs. [default: False]
  --print_args  Print the argument block.
'''

from __future__ import print_function

from docopt import docopt


def parse_orbital_localization_block(outputfile, args):
    ''''''
    spin_map = {
        0: 'alpha',
        1: 'beta'
    }
    line = next(outputfile)
    # Parse the info block before the localization iterations.
    while 'Initial value of the localization sum' not in line:
        # Is this localization block for alpha or beta spin orbitals?
        if 'Operator' in line:
            spin = spin_map.get(int(line.split()[-1]))
        # Is this localization block for occupied or virtual orbitals?
        elif 'Orbital range for localization' in line:
            mo_index_first = int(line.split()[5])
            mo_index_last = int(line.split()[7])
            if mo_index_first == 0:
                orb_block = 'occ'
            else:
                orb_block = 'virt'
        # What localization algorithm are we using? (FB or PM)
        elif 'Localization criterion' in line:
            loc_method = line.split()[3]
        line = next(outputfile)
    line = next(outputfile)
    print('## {} {} {} {}'.format(spin, orb_block, mo_index_first, mo_index_last))
    while 'LOCALIZATION' not in line:
        sline = line.split()
        iteration = int(sline[1])
        try:
            L = float(sline[4])
            DL = float(sline[6])
            max_T = float(sline[8])
        except ValueError:
            L = float(sline[3][2:])
            DL = float(sline[5])
            max_T = float(sline[7])
        line = next(outputfile)
    print('### {} {} {} {}'.format(iteration, L, DL, max_T))
    print(line.strip())
    while 'FOUND' not in line:
        line = next(outputfile)
    while 'Rather strongly localized orbitals' not in line:
        line = next(outputfile)
    # Print the summary of strongly localized orbitals.
    while 'Bond-like localized orbitals' not in line:
        if not args['--only-bond-like']:
            print(line.strip())
        line = next(outputfile)
    # Print the summary of bond-like localized orbitals.
    while "Localized MO's were stored in" not in line:
        print(line.strip())
        line = next(outputfile)



def main(args):
    outputfilename = args['<outputfilename>']
    print('-' * 78)
    print('# {}'.format(outputfilename))

    with open(outputfilename) as outputfile:
        for line in outputfile:
            if 'ORCA ORBITAL LOCALIZATION' in line:
                parse_orbital_localization_block(outputfile, args)

    print('-' * 78)

if __name__ == '__main__':

    args = docopt(__doc__)

    if args['--print_args']:
        print(args)

    main(args)
