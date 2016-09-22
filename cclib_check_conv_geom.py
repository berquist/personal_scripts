#!/usr/bin/env python

"""cclib.check_conv_geom.py: Check if a geometry optimization job
has converged."""

from __future__ import print_function

from .utils import find_string_in_file


def main():
    """Given a set of geometry optimization jobs, determine if they've
    converged.
    """

    import argparse
    from cclib.io import ccopen

    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs = '+')
    args = parser.parse_args()
    filenames = args.filenames

    for filename in filenames:

        job = ccopen(filename)
        # We don't need to parse the output for "traditional" data, we
        # just want to determine the type of file.
        # data = job.parse()

        if type(job) == 'cclib.parser.orcaparser.ORCA':
            string = 'THE OPTIMIZATION HAS CONVERGED'
        elif type(job) == 'cclib.parser.qchemparser.QChem':
            string = ''
        else:
            string = ''

        converged = find_string_in_file(filename, string)
        print('{}: {}'.format(filename, converged))


if __name__ == "__main__":

    main()
