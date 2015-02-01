#!/usr/bin/env python

"""orca.basis_conv.int.write_file.py: Convert a GAMESS-US formatted
basis file from EMSL into something usable by ORCA as an internal
basis. Write to an automatically-named file rather than stdout.
"""


if __name__ == "__main__":

    import argparse

    from orcaparse.basis_utils import convert_basis_int

    # pylint: disable=C0103
    parser = argparse.ArgumentParser()
    parser.add_argument('inp_filename', nargs='+')
    args = parser.parse_args()

    for inp_filename in args.inp_filename:

        with open(inp_filename) as inp_file:
            inp_file_contents = inp_file.read()

        # making an assumption here...
        basis_name = inp_filename.split('.')[1]
        out_filename = 'orca.' + basis_name + '.bas'
        with open(out_filename, 'w') as out_file:
            out_file.write(convert_basis_int(inp_file_contents))
        print(out_filename)
