#!/usr/bin/env python

from __future__ import print_function

from copy import deepcopy


def make_file_iterator(filename):
    """Return an iterator over the contents of the given file name."""
    # pylint: disable=C0103
    with open(filename) as f:
        contents = f.read()
    return iter(contents.splitlines())


def template_input_freq(**rem):
    """The template for a input file that performs a frequency calculation."""
    # If any of these keywords are present in the rem we've passed in,
    # add them to the new input file.
    desired_keywords = (
        'method',
        'exchange',
        'correlation',
        'basis',
        'aux_basis',
        'scf_convergence',
        'scf_guess',
        'scf_algorithm',
        'thresh',
        'xc_grid',
        'mem_static',
        'mem_total',
    )
    # Gather all the potential keywords for the new input file.
    rem_pieces = []
    for k in desired_keywords:
        if k in rem:
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


if __name__ == '__main__':
    import argparse
    import os
    import cclib
    from cclib.parser.utils import PeriodicTable

    pt = PeriodicTable()
    # Format string template for the XYZ section.
    s = '{:3s} {:15.10f} {:15.10f} {:15.10f}'

    parser = argparse.ArgumentParser()
    parser.add_argument('inputfilename', nargs='+')

    args = parser.parse_args()
    inputfilenames = args.inputfilename

    for inputfilename in inputfilenames:

        # Ugly munging to determine the name of the file we're
        # writing.
        splitext = os.path.splitext(inputfilename)
        assert splitext[1] == '.out'
        split = splitext[0].split('_')
        index = ['opt' in x for x in split].index(True)
        split[index] = 'freq'
        outputfilename = '_'.join(split) + '.in'

        inputfile = make_file_iterator(inputfilename)

        rem = dict()

        # Parse the $rem section in the repeated 'User input:' section
        # of the output.
        line = ''
        while line.strip() != '$rem':
            line = next(inputfile)
        line = next(inputfile)
        while '$end' not in line:
            sline = line.split()
            k = sline[0].replace('=', '')
            v = sline[-1].replace('=', '')
            rem[k] = v
            line = next(inputfile)

        # Just use cclib to get the charge and multiplicity.
        # while '$molecule' not in line:
        #     line = next(inputfile)
        # line = next(inputfile)
        # rem['charge'], rem['multiplicity'] = map(int, line.split())

        job = cclib.parser.ccopen(inputfilename)
        data = job.parse()

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

        with open(outputfilename, 'w') as outputfile:
            outputfile.write(template_input_freq(**rem))

        print(outputfilename)
