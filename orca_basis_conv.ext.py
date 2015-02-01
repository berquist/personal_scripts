#!/usr/bin/env python

"""orca.basis_conv.ext.py: Convert a GAMESS-US formatted basis file
from EMSL into something usable by ORCA as an external basis.
"""


if __name__ == "__main__":

    import argparse

    from orcaparse.basis_utils import convert_basis_ext

    # pylint: disable=C0103
    parser = argparse.ArgumentParser()
    parser.add_argument('inp_filename')
    parser.add_argument('out_filename')
    args = parser.parse_args()
    inp_filename = args.inp_filename
    out_filename = args.out_filename

    with open(inp_filename) as inp_file:
        inp_file_contents = inp_file.read()

    with open(out_filename, 'w') as out_file:
        out_file.write(convert_basis_ext(inp_file_contents))
