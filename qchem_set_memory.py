#!/usr/bin/env python

"""qchem_set_memory.py: ..."""


def getargs():
    """Gather and return command-line arguments."""

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('inputfile', nargs='+')

    parser.add_argument('--mem_static', type=int)
    parser.add_argument('--mem_total', type=int)
    parser.add_argument('--cc_memory', type=int)

    args = parser.parse_args()

    return args


def main(args):

    for inputfilename in args.inputfile:

        with open(inputfilename) as inputfile:
            inputfile_lines = inputfile.readlines()

        t = ' {} = {}\n'.format

        for idx, line in enumerate(inputfile_lines):
            if '$rem' in line:
                iidx = idx + 1
                if args.mem_static:
                    inputfile_lines.insert(iidx, t('mem_static', args.mem_static))
                if args.mem_total:
                    inputfile_lines.insert(iidx, t('mem_total', args.mem_total))
                if args.cc_memory:
                    inputfile_lines.insert(iidx, t('cc_memory', args.cc_memory))

        with open(inputfilename, 'w') as inputfile:
            inputfile.write(''.join(inputfile_lines))


if __name__ == '__main__':
    args = getargs()
    main_locals = main(args)
