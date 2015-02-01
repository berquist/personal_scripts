#!/usr/bin/env python

"""utils.py: Utility functions and classes shared by other scripts."""


def read_binary(binaryfilename):
    """Return the bytes present in the given binary file name."""
    with open(binaryfilename, 'rb') as binaryfile:
        readbytes = binaryfile.read()
    return readbytes


def make_file_iterator(filename):
    """Return an iterator over the contents of the given file name."""
    with open(filename) as f:
        contents = f.read()
    return iter(contents.splitlines())


if __name__ == "__main__":
    # Don't use this file as a standalone script.
    pass
