#!/usr/bin/env python

"""gamess_basis_rename.py: Rename all the element labels in the given
basis set file from symbols from full names to symbols.
"""

from __future__ import print_function

from scripts.periodic_table import Name as s2n


def invert_dict(d):
    """Create the inverse/reverse map of a dictionary."""

    return {v:k for (k, v) in d.items()}


def invert_dict_lowercase_vals(d):
    """Create the inverse/reverse map of a dictionary and make the old
    values/new keys lowercase.
    """

    return {v.lower():k for (k, v) in d.items()}


def rename_elements(basfile, mapdict):
    """Rename all the element labels in the basis file according to given
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

    # pylint: disable=C0103
    parser = argparse.ArgumentParser()
    parser.add_argument('basfilename')
    args = parser.parse_args()

    # Create the reverse map: full name to symbol
    n2s = invert_dict_lowercase_vals(s2n)

    with open(args.basfilename) as basfile:
        newbasfile = rename_elements(basfile, n2s)

    print(newbasfile)
