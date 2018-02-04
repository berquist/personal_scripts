#!/usr/bin/env python3

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
from cclib.io import ccopen
from itertools import zip_longest
import re


def parse_line(line, max_mo_index, orbitals, spin):
    """Parse a single line of an orbital composition section."""
    split = line.split()
    idx_atom_element = split[0]
    m = re.search("(\d*)", idx_atom_element)
    idx_atom = int(m.groups()[0])
    element = split[0][m.lastindex:]
    orbital_name = split[1]
    contribs = [float(x) for x in split[2:]]
    mo_indices = list(range(max_mo_index - len(contribs), max_mo_index))
    for i, contrib in enumerate(contribs):
        entry = (idx_atom, element, orbital_name, contrib, spin)
        try:
            orbitals[mo_indices[i]].append(entry)
        except KeyError:
            orbitals[mo_indices[i]] = [entry]


def parse_section(outputfile, nmo, energies, occupations, orbitals, has_beta):
    """Parse an entire orbital composition section. There are at most two
    blocks within each section, one each for alpha and beta spin.
    """
    alpha, beta = 0, 1
    # Skip the dashes and the threshold for printing.
    next(outputfile)
    next(outputfile)
    # "SPIN UP"
    if has_beta:
        # Blank line only for unrestricted calculations.
        next(outputfile)
    parse_block(outputfile, nmo, energies, occupations, orbitals, alpha)
    # "SPIN DOWN"
    next(outputfile)
    if has_beta:
        parse_block(outputfile, nmo, energies, occupations, orbitals, beta)


def parse_block(outputfile, nmo, energies, occupations, orbitals, spin):
    """Parse an entire block (alpha or beta spin) of an orbital
    composition section
    ."""
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
    """Return the AOs that fall within a certain contribution to a single
    MO.
    """
    neworbitals = dict()
    for mo_index in orbitals.keys():
        if mo_index <= max_orbital:
            for contrib in orbitals[mo_index]:
                if contrib[3] >= threshold:
                    try:
                        neworbitals[mo_index].append(contrib)
                    except KeyError:
                        neworbitals[mo_index] = [contrib]
    return neworbitals


def pretty_print_orbitals(energies, orbitals, nmo, has_beta):
    """Pretty-print a set of orbitals and their energies."""
    spins = {0: 'alpha', 1: 'beta'}
    if not has_beta:
        header_template  = ' {key} {en_alpha}'
        contrib_template = '  {:3} {:2} {:5} {:5}'
    else:
        header_template  = ' {key} {en_alpha} {en_beta}'
        contrib_template = '  {:3} {:2} {:5} {:5} {spin:5}'
    for key in orbitals.keys():
        header_dict = {'key': key,
                       'en_alpha': energies[key],
                       'en_beta': energies[key + (has_beta * nmo)]}
        print(header_template.format(**header_dict))
        for contrib in orbitals[key]:
            print(contrib_template.format(*contrib[0:4], spin=spins[contrib[4]]))


def pretty_print_orbitals_dual(results):
    """From two sets of results, print them side-by-side."""
    energies1 = results['energies1']
    energies2 = results['energies2']
    occupations1 = results['occupations1']
    occupations2 = results['occupations2']
    orbitals1 = results['orbitals1']
    orbitals2 = results['orbitals2']
    nmo1 = len(orbitals1)
    nmo2 = len(orbitals2)
    if len(energies1) == 2*len(orbitals1):
        has_beta = True
    else:
        has_beta = False
    spins = {0: 'alpha', 1: 'beta'}
    # Handle the restricted case.
    if not has_beta:
        # header_template_full
        # contrib_template_full
        header_template_left   = ' {key} {en_alpha}'
        contrib_template_left  = '  {:3} {:2} {:5} {:5}'
        # header_template_right
        # contrib_template_right
    # Handle the unrestricted case.
    else:
        # header_template_full
        # contrib_template_full
        header_template_left   = ' {key} {en_alpha} {en_beta}'
        contrib_template_left  = '  {:3} {:2} {:5} {:5} {spin:5}'
        # header_template_right
        # contrib_template_right
    for key1, key2 in izip_longest(orbitals1.keys(), orbitals2.keys()):
        header_dict = {
            'key1': key1,
            'en_alpha1': energies1[key1],
            'en_beta1': energies1[key1 + (has_beta * nmo1)],
            'key2': key2,
            'en_alpha2': energies2[key2],
            'en_beta2': energies2[key2 + (has_beta * nmo2)]
        }
        print(header_template.format(**header_dict))
        for contrib in orbitals[key]:
            print(contrib_template.format(*contrib[0:4], spin=spins[contrib[4]]))


def open_and_parse_outputfile(args, outputfilename):
    """The main routine for opening and parsing each output file."""
    # ORCA prints 6 columns at a time for these types of blocks.
    ncols = 6

    headers = [
        'LOEWDIN ORBITAL POPULATIONS PER MO',
        'LOEWDIN REDUCED ORBITAL POPULATIONS PER MO',
        #'LOEWDIN REDUCED ORBITAL POPULATIONS PER UNO',
        # 'LOEWDIN REDUCED ORBITAL POPULATIONS PER UNSO',
        # This is equivalent to the reduced orbital population per MO, but
        # named differently within CASSCF/MRCI jobs.
        'LOEWDIN ORBITAL-COMPOSITIONS'
    ]

    energies = list()
    occupations = list()
    orbitals = dict()

    # Pre-determine the number of MOs present and whether or not there
    # are two sets of canonical MOs.
    job = ccopen(outputfilename)
    data = job.parse()
    nmo = data.nmo
    has_beta = False
    if len(data.homos) == 2:
        has_beta = True

    # For each possible header, parse the section.
    with open(outputfilename) as outputfile:
        for line in outputfile:
            for header in headers:
                if header in line:
                    parsed_header = header
                    print(parsed_header)
                    parse_section(outputfile, nmo, energies, occupations, orbitals, has_beta)

    # determine the last orbital we should be printing information
    # about
    if not args['--max_orbital']:
        args['--max_orbital'] = data.homos[0] * 2
    if args['--max_orbital'] == 'all':
        args['--max_orbital'] = nmo
    max_orbital = int(args['--max_orbital'])

    threshold = float(args['--threshold'])
    filtered_mos = get_orbital_contribs_within_threshold(orbitals, threshold, max_orbital)
    print(parsed_header)
    pretty_print_orbitals(energies, filtered_mos, nmo, has_beta)

    return energies, occupations, orbitals


def main(args):
    """The main routine for determining whether we parse/print one or two
    output files
    ."""

    outputfilename1 = args['<outputfilename>']
    energies1, occupations1, orbitals1 = open_and_parse_outputfile(args, outputfilename1)
    # If we're going to compare two output files side-by-side...
    if args['--dual']:
        outputfilename2 = args['--dual']
        energies2, occupations2, orbitals2 = open_and_parse_outputfile(args, outputfilename2)

    results = {
        'energies1'    : energies1,
        'occupations1' : occupations1,
        'orbitals1'    : orbitals1
    }
    if args['--dual']:
        results['energies2']    = energies2
        results['occupations2'] = occupations2
        results['orbitals2']    = orbitals2
        # If we parse two outputs, clearly we want to print their results
        # side-by-side.
        pretty_print_orbitals_dual(results)

    return results


if __name__ == "__main__":

    args = docopt(__doc__)

    if args['--print_args']:
        print(args)

    main(args)
