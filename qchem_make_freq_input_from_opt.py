#!/usr/bin/env python

"""qchem_make_freq_input_from_opt.py: Make an input file for a Q-Chem
frequency calculation based on the last possible geometry from a
Q-Chem geometry optimization.

The script assumes the output file being read from is called
'*opt(\d*).out', where 'opt' might be followed by a number. The script
will write an input file called '*freq.in'.
"""

from __future__ import print_function

import re

import cclib
from cclib.parser.utils import PeriodicTable

from copy import deepcopy

from qchem_make_opt_input_from_opt import make_file_iterator


def template_input_freq(**rem):
    """The template for a input file that performs a frequency calculation."""
    avoid_these_keywords = (
        'jobtype',
    )
    rem_pieces = []
    for k in rem:
        if k not in avoid_these_keywords:
            rem_pieces.append(' {} = {}'.format(k, rem[k]))
    rem_str = '\n'.join(rem_pieces)
    # Return a string, which is the contents of the new input file,
    # with the '{}' fields appropriately replaced.
    return """$rem
 jobtype = freq
{rem_str}
$end

$molecule
{charge} {multiplicity}
{atoms}
$end
""".format(rem_str=rem_str, **rem)


def clean_up_rem(rem):
    """Make sure our $rem section is stringent enough for frequency
    calculations.
    """

    # These are the minimum values we'd like for frequency
    # calculations.
    min_scf_convergence = 9
    min_thresh = 12

    newrem = deepcopy(rem)
    if 'thresh' in newrem:
        if int(newrem['thresh']) < min_thresh:
            newrem['thresh'] = min_thresh
    if 'scf_convergence' in newrem:
        if int(newrem['scf_convergence']) < min_scf_convergence:
            newrem['scf_convergence'] = min_scf_convergence

    return newrem


def getargs():
    """Get command-line arguments."""

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('outputfilename', nargs='+')

    args = parser.parse_args()

    return args


def parse_rem_section(outputfilename):
    """Parse the $rem section in the repeated 'User input:' section of the
    output.
    """

    outputfile = make_file_iterator(outputfilename)

    rem = dict()

    line = ''
    while line.strip().lower() != '$rem':
        line = next(outputfile)
    line = next(outputfile)
    while '$end' not in line:
        sline = line.split()
        k = sline[0].replace('=', '').lower()
        v = sline[-1].replace('=', '').lower()
        rem[k] = v
        line = next(outputfile)

    return rem


if __name__ == '__main__':

    args = getargs()

    pt = PeriodicTable()
    # Format string template for the XYZ section.
    s = '{:3s} {:15.10f} {:15.10f} {:15.10f}'

    for outputfilename in args.outputfilenames:

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
        assert inputfilename.endswith('.out')
        inputfilename = re.sub(r'opt\d*', 'freq', outputfilename).replace('.out', '.in')

        rem = parse_rem_section(outputfilename)

        rem['charge'] = data.charge
        rem['multiplicity'] = data.mult

        # Make sure our $rem section is up to snuff for frequency
        # calculations.
        rem = clean_up_rem(rem)

        # Form the atomic symbols and coordinates for each atom in
        # $molecule.
        last_geometry = data.atomcoords[-1]
        element_list = [pt.element[Z] for Z in data.atomnos]
        rem['atoms'] = '\n'.join(s.format(element, *coords)
                                 for element, coords in zip(element_list, last_geometry))

        with open(inputfilename, 'w') as inputfile:
            inputfile.write(template_input_freq(**rem))

        print(inputfilename)
