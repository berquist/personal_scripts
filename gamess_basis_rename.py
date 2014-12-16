#!/usr/bin/env python

from __future__ import print_function
from periodic_table import Name as s2n


def invert_dict(d):
    """Create the inverse/reverse map of a dictionary."""
    return {v:k for k, v in d.items()}


def rename_elements(basfile, mapdict):
    """Rename all the element labels in the basis file accoding to given
    map.
    """
    newbasfile = []
    for line in basfile:
        for k in mapdict:
            if k.lower() in line.lower():
                line = line.lower().replace(k.lower(), mapdict.get(k))
        newbasfile.append(line)
    return "".join(newbasfile)

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('basfilename')
    args = parser.parse_args()
    basfilename = args.basfilename

    # Create the reverse map: full name to symbol
    n2s = invert_dict(s2n)

    with open(basfilename) as basfile:
        newbasfile = rename_elements(basfile, n2s)

    print(newbasfile)
