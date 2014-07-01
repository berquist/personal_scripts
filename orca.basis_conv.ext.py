#!/usr/bin/env python

'''orca.basis_conv.ext.py: Convert a GAMESS-US formatted basis file from
EMSL into something usable by ORCA as an external basis.'''

if __name__ == '__main__':

    import argparse

    from orcaparse.basis_utils import convert_basis_ext

    parser = argparse.ArgumentParser()
    parser.add_argument('inp_filename')
    parser.add_argument('out_filename')
    args = parser.parse_args()
    inp_filename = args.inp_filename
    out_filename = args.out_filename

    inp_file = open(inp_filename, 'rb')
    inp_file_contents = inp_file.read()
    inp_file.close()

    out_file = open(out_filename, 'wb')
    out_file.write(convert_basis_ext(inp_file_contents))
    out_file.close()
