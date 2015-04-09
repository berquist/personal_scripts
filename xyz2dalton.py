#!/usr/bin/env python

"""xyz2dalton.py: Given an XYZ file, convert the coordinates to input
suitable for a DALTON calculation, with the option to use either the
built-in periodic table, cclib, or Open Babel.
"""

from __future__ import print_function


def main():
    """"""

    import argparse
    import os.path
    import sys
    from itertools import count as counter

    parser = argparse.ArgumentParser()

    parser.add_argument('convertor', choices=('builtin', 'openbabel', 'cclib'))
    parser.add_argument('xyzfilename', nargs='+')

    args = parser.parse_args()
    xyzfilenames = args.xyzfilename

    for xyzfilename in xyzfilenames:

        # outfilename = ''.join([os.path.splitext(xyzfilename)[0], '.dal'])

        if args.convertor == 'openbabel':
            import subprocess as sp
            ob_output = sp.check_output(['obabel', '-ixyz', xyzfilename, '-odalmol']).decode('utf-8')
            ob_splitlines = ob_output.splitlines()
            # with open(outfilename, 'w') as outfile:
            #     outfile.write('\n'.join(ob_splitlines))
            print(ob_splitlines)
        elif args.convertor == 'cclib':
            sys.exit()
        elif args.convertor == 'builtin':
            from scripts.periodic_table import AtomicNum
            with open(xyzfilename) as xyzfile:
                xyzfile_contents = xyzfile.read()
            xyzfile_splitlines = xyzfile_contents.splitlines()[2:]
            outfilelines = []
            atomtypes = 0
            atomsymbols = (line.split()[0] for line in xyzfile_splitlines)
            atomnums = (float(AtomicNum[symbol]) for symbol in atomsymbols)
            oldcharge = ''
            count = 0
            for i, atomnum, line in zip(counter(start=1), atomnums, xyzfile_splitlines):
                newcharge = atomnum
                if newcharge != oldcharge and i > 1:
                    atom_section_header = 'Charge={charge} Atoms={count}'.format(charge=oldcharge, count=count)
                    outfilelines.insert(len(outfilelines) - count, atom_section_header)
                    count = 0
                    atomtypes += 1
                outfilelines.append(line)
                count += 1
                oldcharge = newcharge
            atom_section_header = 'Charge={charge} Atoms={count}'.format(charge=oldcharge, count=count)
            outfilelines.insert(len(outfilelines) - count, atom_section_header)
            atomtypes += 1
            mol_section_header = 'Atomtypes={atomtypes} Angstrom Nosymmetry'.format(atomtypes=atomtypes)
            outfilelines.insert(0, mol_section_header)
            print('\n'.join(outfilelines))
        else:
            sys.exit()


if __name__ == "__main__":
    main()
