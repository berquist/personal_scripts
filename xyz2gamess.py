#!/usr/bin/env python

"""xyz2gamess.py: Given an XYZ file, convert the coordinates to input
suitable for a GAMESS calculation, with the option to use either the
built-in periodic table, cclib, or Open Babel.
"""

from __future__ import print_function


def main():
    """"""

    import argparse
    import os.path

    parser = argparse.ArgumentParser()

    parser.add_argument('xyzfilename', nargs='+')
    parser.add_argument('--use-openbabel', action='store_true')
    # TODO
    parser.add_argument('--use-cclib', action='store_true')

    args = parser.parse_args()
    xyzfilenames = args.xyzfilename

    for xyzfilename in xyzfilenames:

        outfilename = ''.join([os.path.splitext(xyzfilename)[0], '.inp'])

        if args.use_openbabel:
            import subprocess as sp
            ob_output = sp.check_output(['obabel', '-ixyz', xyzfilename, '-ogamin']).decode('utf-8')
            ob_splitlines = ob_output.splitlines()[5:-3]
            with open(outfilename, 'w') as outfile:
                outfile.write('\n'.join(ob_splitlines))
        else:
            from scripts.periodic_table import AtomicNum
            with open(xyzfilename) as xyzfile:
                xyzfile_contents = xyzfile.read()
            xyzfile_splitlines = xyzfile_contents.splitlines()[2:]
            with open(outfilename, 'w') as outfile:
                for line in xyzfile_splitlines:
                    sline = line.strip().split()
                    symbol, x, y, z = sline
                    atomnum = float(AtomicNum[symbol])
                    atom = ' {} {} {} {} {}\n'.format(symbol, atomnum, x, y, z)
                    outfile.write(atom)

if __name__ == "__main__":
    main()
