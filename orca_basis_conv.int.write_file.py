#!/usr/bin/env python

'''orca.basis_conv.int.write_file.py: Convert a GAMESS-US formatted basis file
from EMSL into something usable by ORCA as an internal basis. Write to an
automatically-named file rather than stdout.'''

if __name__ == '__main__':

    import argparse

    from orcaparse.basis_utils import convert_basis_int

    parser = argparse.ArgumentParser()
    parser.add_argument('inp_filename', nargs='+')
    args = parser.parse_args()

    for inp_filename in args.inp_filename:

        inp_file = open(inp_filename, 'rb')
        inp_file_contents = inp_file.read()
        inp_file.close()

        # making an assumption here...
        basis_name = inp_filename.split('.')[1]
        out_filename = 'orca.' + basis_name + '.bas'
        out_file = open(out_filename, 'wb')
        out_file.write(convert_basis_int(inp_file_contents))
        out_file.close()
        print(out_filename)
