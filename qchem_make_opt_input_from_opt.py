#!/usr/bin/env python

"""qchem_make_opt_input_from_opt.py: Make an input file for a Q-Chem
geometry optimization based on the last possible geometry from a
Q-Chem geometry optimization; this effectively 'restarts' the geometry
with a new filename.

The script assumes the output file being read from is called
'*opt(\d*).out', where 'opt' might be followed by a number. The script
will write an input file called '*opt(\d*)+1.in', with the previous
number incremented by one.
"""

from __future__ import print_function

import re

import cclib
from cclib.parser.utils import PeriodicTable


def make_file_iterator(filename):
    """Return an iterator over the contents of the given file name."""
    # pylint: disable=C0103
    with open(filename) as f:
        contents = f.read()
    return iter(contents.splitlines())


def getargs():
    """Get command-line arguments."""

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('outputfilename', nargs='+')

    args = parser.parse_args()

    return args


def parse_user_input(outputfilename):
    """Parse the $rem section in the repeated 'User input:' section of the
    output.

    The reason we do it this way rather than with shell tools is to
    handle any $section more easily and in a case-insensitive manner.
    """

    user_input = dict()

    outputfile = make_file_iterator(outputfilename)

    line = ''
    while 'User input:' not in line:
        line = next(outputfile)
    line = next(outputfile)
    assert '----' in line
    line = next(outputfile)
    while '--------------------------------------------------------------' not in line:
        if line.strip() == '':
            pass
        elif line[0] == '$' and line.strip().lower() != '$end':
            section_header = line[1:].lower()
            user_input[section_header] = []
        elif line.strip().lower() == '$end':
            user_input[section_header] = '\n'.join(user_input[section_header])
        else:
            user_input[section_header].append(line)
        line = next(outputfile)

    return user_input


if __name__ == '__main__':

    args = getargs()

    pt = PeriodicTable()
    # Format string template for the XYZ section.
    s = '{:3s} {:15.10f} {:15.10f} {:15.10f}'

    for outputfilename in args.outputfilename:

        job = cclib.parser.ccopen(outputfilename)
        assert isinstance(job, cclib.parser.qchemparser.QChem)
        try:
            data = job.parse()
        # this is to deal with the Q-Chem parser not handling
        # incomplete SCF cycles properly
        except StopIteration:
            print('no output made: StopIteration in {}'.format(outputfilename))
            continue

        # Determine the name of the file we're writing.
        assert outputfilename.endswith('.out')
        numstr = re.search(r'opt(\d*).out$', outputfilename).groups()[0]
        if numstr == '':
            optnum = 2
        else:
            optnum = int(numstr) + 1
        inputfilename = re.sub(r'opt\d*', 'opt{}'.format(optnum), outputfilename).replace('.out', '.in')

        user_input = parse_user_input(outputfilename)

        # Form the atomic symbols and coordinates for each atom in
        # $molecule.
        element_list = (pt.element[Z] for Z in data.atomnos)
        last_geometry = data.atomcoords[-1]
        molecule_section = ['{} {}'.format(data.charge, data.mult)]
        for element, coords, in zip(element_list, last_geometry):
            molecule_section.append(s.format(element, *coords))
        user_input['molecule'] = '\n'.join(molecule_section)

        with open(inputfilename, 'w') as fh:
            for section_header in user_input:
                fh.write('${}\n'.format(section_header))
                fh.write(user_input[section_header])
                fh.write('\n$end\n\n')

        print(inputfilename)
