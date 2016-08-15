#!/usr/bin/env python

from __future__ import print_function
from __future__ import division

from itertools import zip_longest


def getargs():
    """Parse command-line arguments."""

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('file',
                        nargs='+',
                        help="""""")
    parser.add_argument('--num-per-group',
                        type=int,
                        default=0,
                        help="""""")
    parser.add_argument('--action',
                        choices=('copy', 'move'),
                        help="""""")

    args = parser.parse_args()

    return args


def grouper(n, iterable, fillvalue=None):
    """grouper(3, 'ABCDEFG', 'x') --> ['ABC', 'DEF', 'Gxx']"""
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


def main(args):

    import shutil
    import os

    if args.action == 'copy':
        action = shutil.copy2
    elif args.action == 'move':
        action = shutil.move
    else:
        action = print

    for groupnum, group in enumerate(grouper(args.num_per_group, args.file), start=1):
        try:
            dest = os.path.join(os.getcwd(), 'group_{}'.format(groupnum))
            os.mkdir(dest, mode=0o755)
        except:
            pass
        for f in (i for i in group if i):
            action(f, dest)

    return locals()


if __name__ == "__main__":

    args = getargs()
    main_locals = main(args)
