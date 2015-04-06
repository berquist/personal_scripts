#!/usr/bin/env python

from __future__ import print_function


def make_file_iterator(filename):
    """Return an iterator over the contents of the given file name."""
    # pylint: disable=C0103
    with open(filename) as f:
        contents = f.read()
    return iter(contents.splitlines())


def template_freq_input(**rem):
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
        'xc_grid'
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

        splitext = os.path.splitext(inputfilename)
        assert splitext[1] == '.out'
        stub = '_'.join(splitext[0].split('_')[1:])
        outputfilename = 'freq_{}.in'.format(stub)

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

        # Form the atomic symbols and coordinates for each atom in
        # $molecule.
        last_geometry = data.atomcoords[-1]
        element_list = [pt.element[Z] for Z in data.atomnos]
        rem['atoms'] = '\n'.join(s.format(element, *coords)
                                 for element, coords in zip(element_list, last_geometry))

        with open(outputfilename, 'w') as outputfile:
            outputfile.write(template_freq_input(**rem))
