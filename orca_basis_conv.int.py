#!/usr/bin/env python

"""orca.basis_conv.int.py: Convert a GAMESS-US formatted basis file
from EMSL into something usable by ORCA as an internal basis.
"""


if __name__ == "__main__":

    import argparse
    import sys

    from orcaparse.basis_utils import convert_basis_int

    # pylint: disable=C0103
    parser = argparse.ArgumentParser()
    parser.add_argument('inp_filename')
    args = parser.parse_args()
    inp_filename = args.inp_filename

    with open(inp_filename) as inp_file:
        inp_file_contents = inp_file.read()

    out_file = sys.stdout
    out_file.write(convert_basis_int(inp_file_contents))
