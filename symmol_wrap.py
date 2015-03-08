#!/usr/bin/env python

'''symmol_generate_input.py: Generate an input appropriate for the
Fortran 77 program SYMMOL. Send the input to stdout.

Usage:
  symmol_wrap.py [options] <xyzfilename>

Options:
  --tol1=TOL1   Set the tolerance for ... [Default: 1.0]
  --tol2=TOL2   Set the tolerance for ... [Default: 1.0]
  --print_args  Print the docopt argument block.
'''

from __future__ import print_function

from docopt import docopt
from itertools import count

from scripts.xyz_rotate_by_angle import read_xyz_file


def create_formatted_symmol_input(structure, tol1, tol2, comment=''):
    """From a geometry, format the SYMMOL input properly.

    The formatting is dictated by the following line from the source code:
      READ(RIGA,'(A6,I2,6f9.5)')NAME(i),MOL(i),(X(k,i),k=1,3),
    where the variables are defined as:
      PARAMETER (NMA=1000)
      CHARACTER*80 RIGA
      COMMON/AT1/X(3,NMA)
      COMMON/AT3/MOL(NMA)
      CHARACTER*6 NAME
      COMMON/AT4/NAME(NMA)
    """
    header_template = ''' 1 1 1 90 90 90\n 1 1 {tol1:4.3f} {tol2:4.3f}'''
    header = header_template.format(tol1=tol1, tol2=tol2)
    comment_line = '# ' + comment
    formatted_atoms = [comment_line, header]
    template = '{symbol:<6}{derp:2d}{x:9.5f}{y:9.5f}{z:9.5f}'
    for i, atom in zip(count(start=1), structure):
        symbol = atom[0] + str(i)
        formatted_atom = template.format(symbol=symbol,
                                         derp=1,
                                         x=atom[1],
                                         y=atom[2],
                                         z=atom[3])
        formatted_atoms.append(formatted_atom)

    return '\n'.join(formatted_atoms)


def main():
    """If being used as a script, this is the main entry point.
    """
    args = docopt(__doc__)
    if args['--print_args']:
        print(args)

    # Read in the XYZ file.
    xyzfilename = args['<xyzfilename>']
    natoms, comment, structure = read_xyz_file(xyzfilename)

    tol1 = float(args['--tol1'])
    tol2 = float(args['--tol2'])

    symmolinputfile = create_formatted_symmol_input(structure, tol1, tol2)
    print(symmolinputfile)

if __name__ == '__main__':

    main()
