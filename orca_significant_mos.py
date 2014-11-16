#!/usr/bin/env python

'''Parse the reduced MO blocks for ...

Usage:
  orca_significant_mos.py [options] <outputfilename>

Options:
  --threshold=THRESH      Set the printing threshold. [default: 2.0]
  --max_orbital=MAX       Don't print anything above this orbital index. Default to 2*NOcc, can also specify 'all'.
  --dual=outputfilename2  Optionally compare two files.
  --print_args            Print the parsed argument block.
'''

from __future__ import print_function

from docopt import docopt
from cclib.parser import ccopen


def parse_line(line, max_mo_index, orbitals, spin):
    ''''''
    split = line.split()
    idx_atom = int(split[0])
    element = split[1]
    orbital_name = split[2]
    contribs = list(map(float, split[3:]))
    mo_indices = list(range(max_mo_index - len(contribs), max_mo_index))
    for i, contrib in enumerate(contribs):
        entry = (idx_atom, element, orbital_name, contrib, spin)
        try:
            orbitals[mo_indices[i]].append(entry)
        except KeyError:
            orbitals[mo_indices[i]] = [entry]


def parse_section(outputfile, nmo, energies, occupations, orbitals, has_beta):
    ''''''
    alpha, beta = 0, 1
    # Skip the dashes and the threshold for printing.
    next(outputfile)
    next(outputfile)
    # "SPIN UP"
    if has_beta:
        next(outputfile)
    parse_block(outputfile, nmo, energies, occupations, orbitals, alpha)
    # "SPIN DOWN"
    next(outputfile)
    if has_beta:
        parse_block(outputfile, nmo, energies, occupations, orbitals, beta)


def parse_block(outputfile, nmo, energies, occupations, orbitals, spin):
    ''''''
    counter = 0
    while counter < (nmo - 1):
        line = next(outputfile)
        # the first line contains orbital numbers, starting at zero!
        counter = int(line.split()[-1])
        line = next(outputfile)
        # the second line contains energies in Hartree
        energies.extend(map(float, line.split()))
        line = next(outputfile)
        # the third line contains occupation numbers
        occupations.extend(map(float, line.split()))
        line = next(outputfile)
        line = next(outputfile)
        # an arbitrary (>= 1) number of lines contains 9 columns; this is the goods!
        while line != '\n':
            parse_line(line, counter + 1, orbitals, spin)
            line = next(outputfile)


def get_orbital_contribs_within_threshold(orbitals, threshold, max_orbital):
    ''''''
    neworbitals = dict()
    for mo_index in orbitals.iterkeys():
        if mo_index <= max_orbital:
            for contrib in orbitals[mo_index]:
                if contrib[3] >= threshold:
                    try:
                        neworbitals[mo_index].append(contrib)
                    except KeyError:
                        neworbitals[mo_index] = [contrib]
    return neworbitals


def pretty_print_orbitals(energies, orbitals, nmo, has_beta):
    ''''''
    spins = {0: 'alpha', 1: 'beta'}
    if not has_beta:
        header_template = ' {key} {en_alpha}'
        contrib_template = '  {:3} {:2} {:5} {:5}'
    else:
        header_template = ' {key} {en_alpha} {en_beta}'
        contrib_template = '  {:3} {:2} {:5} {:5} {spin:5}'
    for key in orbitals.iterkeys():
        header_dict = {'key': key,
                       'en_alpha': energies[key],
                       'en_beta': energies[key + (has_beta * nmo)]}
        print(header_template.format(**header_dict))
        for contrib in orbitals[key]:
            print(contrib_template.format(*contrib[0:4], spin=spins[contrib[4]]))


def main(args):
    ''''''
    # ORCA prints 6 columns at a time for these types of blocks.
    ncols = 6

    headers = [
        'LOEWDIN ORBITAL POPULATIONS PER MO',
        'LOEWDIN REDUCED ORBITAL POPULATIONS PER MO',
        'LOEWDIN REDUCED ORBITAL POPULATIONS PER UNO',
        # 'LOEWDIN REDUCED ORBITAL POPULATIONS PER UNSO',
        # This is equivalent to the reduced orbital population per MO, but
        # named differently within CASSCF/MRCI jobs.
        'LOEWDIN ORBITAL-COMPOSITIONS'
    ]

    energies = list()
    occupations = list()
    orbitals = dict()

    # pre-determine the number of MOs present and whether or not
    # there are two sets of canonical MOs
    outputfilename = args['<outputfilename>']
    job = ccopen(outputfilename)
    data = job.parse()
    nmo = data.nmo
    has_beta = False
    if len(data.homos) == 2:
        has_beta = True

    with open(outputfilename) as outputfile:
        for line in outputfile:
            for header in headers:
                if header in line:
                    parsed_header = header
                    parse_section(outputfile, nmo, energies, occupations, orbitals, has_beta)

    # determine the last orbital we should be printing information about
    if not args['--max_orbital']:
        args['--max_orbital'] = data.homos[0] * 2
    if args['--max_orbital'] == 'all':
        args['--max_orbital'] = nmo
    max_orbital = int(args['--max_orbital'])

    threshold = float(args['--threshold'])
    filtered_mos = get_orbital_contribs_within_threshold(orbitals, threshold, max_orbital)
    print(parsed_header)
    pretty_print_orbitals(energies, filtered_mos, nmo, has_beta)


if __name__ == '__main__':

    args = docopt(__doc__)

    if args['--print_args']:
        print(args)

    main(args)
