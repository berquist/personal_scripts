#!/usr/bin/env python

'''

Usage:
  orca_print_localization_summary.py [options] <outputfilename>

Options:
  --only-bond-like  Only print the bond-like localized MOs. [default: False]
  --print_args  Print the argument block.
'''


from docopt import docopt


def _parse_strongly_localized_orbitals(outputfile):
    line = next(outputfile)
    while 'MO ' in line:
        print(line.strip())
        line = next(outputfile)


def _parse_bond_like_orbitals(outputfile):
    line = next(outputfile)
    while 'MO ' in line:
        print(line.strip())
        line = next(outputfile)


def _parse_delocalized_orbitals(outputfile):
    line = next(outputfile)
    while 'MO ' in line:
        print(line.strip())
        line = next(outputfile)


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
    num_strongly_localized = int(line.strip().split()[2])
    line = next(outputfile)
    num_bonding = int(line.strip().split()[1])
    line = next(outputfile)
    num_delocalized = int(line.strip().split()[1])
    line = next(outputfile)
    while "Localized MO's were stored in" not in line:
        # Parse the strongly localized orbitals.
        if 'Rather strongly localized orbitals' in line:
            if not args['--only-bond-like']:
                _parse_strongly_localized_orbitals(outputfile)
        # Parse the bond-like localized orbitals.
        if 'Bond-like localized orbitals' in line:
            _parse_bond_like_orbitals(outputfile)
        # Parse the delocalized orbitals.
        if 'More delocalized orbitals' in line:
            _parse_delocalized_orbitals(outputfile)
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
