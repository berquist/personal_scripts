#!/usr/bin/env python

"""qchem_extract_molden.py: ..."""

if __name__ == '__main__':
    import argparse
    import os

    parser = argparse.ArgumentParser()

    parser.add_argument('inputfilename', nargs='+')

    args = parser.parse_args()

    for inputfilename in args.inputfilename:

        outputfilename = os.path.splitext(inputfilename)[0] + '.molden'

        with open(inputfilename) as inputfile:
            for line in inputfile:
                if '======= MOLDEN-FORMATTED INPUT FILE FOLLOWS =======' in line:
                    line = next(inputfile)
                    with open(outputfilename, 'w') as outputfile:
                        while '======= END OF MOLDEN-FORMATTED INPUT FILE =======' not in line:
                            outputfile.write(line)
                            line = next(inputfile)
