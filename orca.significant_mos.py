#!/usr/bin/env python

'''Parse the reduced MO blocks for ...

Usage:
  orca.significant_mos.py [options] (canon | uno) <outputfilename>

Options:
  --threshold=THRESH  Set the printing threshold. [default: 2.0]
  --max_orbital=MAX   Don't print anything above this orbital index. Default to 2*NOcc, can also specify 'all'.
  --print_args        Print the parsed argument block.
'''

# ORCA prints 6 columns at a time for these blocks
ncols = 6

header_mo = 'LOEWDIN REDUCED ORBITAL POPULATIONS PER MO'
header_uno = 'LOEWDIN REDUCED ORBITAL POPULATIONS PER UNO'
# header_unso = 'LOEWDIN REDUCED ORBITAL POPULATIONS PER UNSO'

energies = list()
occupations = list()
orbitals = dict()


def parse_line(line, max_mo_index, spin):
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


def parse_section(outputfile):
    ''''''
    alpha, beta = 0, 1
    # skip the dashes and the threshold for printing
    next(outputfile)
    next(outputfile)
    # "SPIN UP"
    if has_beta and args['canon']:
        next(outputfile)
    parse_block(outputfile, alpha)
    # "SPIN DOWN"
    next(outputfile)
    if has_beta and args['canon']:
        parse_block(outputfile, beta)


def parse_block(outputfile, spin):
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
            parse_line(line, counter + 1, spin)
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


def pretty_print_orbitals(orbitals, has_beta):
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


if __name__ == '__main__':

    from docopt import docopt
    from cclib.parser import ccopen

    args = docopt(__doc__)

    if args['--print_args']:
        print(args)

    # pre-determine the number of MOs present and whether or not
    # there are two sets of canonical MOs
    outputfilename = args['<outputfilename>']
    job = ccopen(outputfilename)
    data = job.parse()
    nmo = data.nmo
    has_beta = False
    if len(data.homos) == 2:
        has_beta = True

    if args['canon']:
        header = header_mo
    if args['uno']:
        header = header_uno

    with open(outputfilename) as outputfile:
        for line in outputfile:
            if header in line:
                parse_section(outputfile)

    # determine the last orbital we should be printing information about
    if not args['--max_orbital']:
        args['--max_orbital'] = data.homos[0] * 2
    if args['--max_orbital'] == 'all':
        args['--max_orbital'] = nmo
    max_orbital = int(args['--max_orbital'])

    threshold = float(args['--threshold'])
    filtered_mos = get_orbital_contribs_within_threshold(orbitals, threshold, max_orbital)
    print(header)
    pretty_print_orbitals(filtered_mos, has_beta)
