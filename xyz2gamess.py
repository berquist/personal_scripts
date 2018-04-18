#!/usr/bin/env python

"""xyz2gamess.py: Given an XYZ file, convert the coordinates to input
suitable for a GAMESS calculation, with the option to use either the
built-in periodic table, cclib, or Open Babel.
"""

from __future__ import print_function


def main():
    """If used as a script, the main routine."""

    import argparse
    import os.path
    import sys

    parser = argparse.ArgumentParser()

    arg = parser.add_argument
    arg('convertor', choices=('builtin', 'openbabel', 'cclib'))
    arg('xyzfilename', nargs='+')
    arg('--to-files', action='store_true')

    args = parser.parse_args()
    xyzfilenames = args.xyzfilename

    for xyzfilename in xyzfilenames:

        outfilename = ''.join([os.path.splitext(xyzfilename)[0], '.inp'])

        if args.convertor == 'openbabel':
            import subprocess as sp
            ob_output = sp.check_output(['obabel',
                                         '-ixyz', xyzfilename,
                                         '-ogamin']).decode('utf-8')
            ob_splitlines = ob_output.splitlines()[5:-3]
            output = '\n'.join(ob_splitlines)
        elif args.convertor == 'cclib':
            print("cclib-based converter not implemented yet", file=sys.stderr)
            sys.exit(1)
        elif args.convertor == 'builtin':
            from periodic_table import AtomicNum
            with open(xyzfilename) as xyzfile:
                xyzfile_contents = xyzfile.read()
            xyzfile_splitlines = xyzfile_contents.splitlines()[2:]
            atoms = []
            for line in xyzfile_splitlines:
                sline = line.strip().split()
                symbol, x, y, z = sline
                atomnum = float(AtomicNum[symbol])
                atom = ' {} {} {} {} {}'.format(symbol, atomnum, x, y, z)
                atoms.append(atom)
            output = '\n'.join(atoms)
        else:
            sys.exit()

        if args.to_files:
            _file = open(outputfilename, 'w')
        else:
            _file = sys.stdout
        print(output, file=_file)
        if args.to_files:
            _file.close()


if __name__ == "__main__":
    main()
