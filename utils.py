#!/usr/bin/env python

"""utils.py: Utility functions and classes shared by other scripts."""


def read_binary(binaryfilename):
    """Return the bytes present in the given binary file name."""
    with open(binaryfilename, 'rb') as binaryfile:
        readbytes = binaryfile.read()
    return readbytes


def make_file_iterator(filename):
    """Return an iterator over the contents of the given file name."""
    # pylint: disable=C0103
    with open(filename) as f:
        contents = f.read()
    return iter(contents.splitlines())


def find_string_in_file(filename, string):
    """Does the give string occur anywhere within the file with the given
    name?
    """
    # pylint: disable=C0103
    with open(filename) as f:
        for line in f:
            if string in line:
                return True
    return False


if __name__ == "__main__":
    # Don't use this file as a standalone script.
    pass
