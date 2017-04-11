#!/usr/bin/env python

"""xyz2dalton.py: Given an XYZ file, convert the coordinates to input
suitable for a DALTON calculation, with the option to use either the
built-in periodic table, cclib, or Open Babel.
"""

from __future__ import print_function

from itertools import count as counter


def xyz2dalton_from_file(xyzfilename, totalcharge=0):
    """A wrapper around xyz2dalton_from_splitlines() that will open an XYZ
    file with the given name.
    """

    with open(xyzfilename) as xyzfile:
        xyzfile_contents = xyzfile.read()
    xyzfile_splitlines = xyzfile_contents.splitlines()[2:]
    outfilecontents = xyz2dalton_from_splitlines(xyzfile_splitlines, totalcharge)

    return outfilecontents


def xyz2dalton_from_splitlines(xyzfile_splitlines, totalcharge=0):
    """Given a list of lines from an XYZ file (not the # of atoms or
    comment lines!), format the file contents into a section suitable for
    DALTON's MOLECULE input section.
    """

    from scripts.periodic_table import AtomicNum

    outfilelines = []
    atomtypes = 0
    atomsymbols = [line.split()[0] for line in xyzfile_splitlines if line.strip() != '']
    atomnums = [float(AtomicNum[symbol]) for symbol in atomsymbols]
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
    mol_section_header = 'Atomtypes={atomtypes} Angstrom Charge={totalcharge} Nosymmetry'.format(atomtypes=atomtypes, totalcharge=totalcharge)
    outfilelines.insert(0, mol_section_header)

    return '\n'.join(outfilelines)


def main():
    """If used as a script, the main routine."""

    import argparse
    import sys

    parser = argparse.ArgumentParser()

    parser.add_argument('convertor', choices=('builtin', 'openbabel', 'cclib'))
    parser.add_argument('xyzfilename', nargs='+')
    parser.add_argument('--charge', type=int, default=0)

    args = parser.parse_args()
    xyzfilenames = args.xyzfilename

    for xyzfilename in xyzfilenames:

        if args.convertor == 'openbabel':
            import subprocess as sp
            ob_output = sp.check_output(['obabel', '-ixyz', xyzfilename, '-odalmol']).decode('utf-8')
            ob_splitlines = ob_output.splitlines()
            print(ob_splitlines)
        elif args.convertor == 'cclib':
            print("cclib-based converter not implemented yet", file=sys.stderr)
            sys.exit()
        elif args.convertor == 'builtin':
            output = xyz2dalton_from_file(xyzfilename, args.charge)
            print(output)
        else:
            sys.exit()


if __name__ == "__main__":
    main()
