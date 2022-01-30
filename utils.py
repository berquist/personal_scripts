#!/usr/bin/env python

"""utils.py: Utility functions and classes shared by other scripts."""

import re


def read_binary(binaryfilename):
    """Return the bytes present in the given binary file name."""
    with open(binaryfilename, "rb") as binaryfile:
        readbytes = binaryfile.read()
    return readbytes


def make_file_iterator(filename):
    """Return an iterator over the contents of the given file name."""
    # pylint: disable=C0103
    with open(filename) as f:
        contents = f.read()
    return iter(contents.splitlines())


def one_largest(inlist):
    """Return the largest item from the sequence."""
    if len(inlist) == 1:
        return inlist[0]
    if inlist[0] > inlist[1]:
        largest = inlist[0]
    else:
        largest = inlist[1]
    for item in inlist[2:]:
        if item > largest:
            largest = item
    return largest


def two_largest(inlist):
    """Return the two largest items in the sequence. The sequence must
    contain at least two items.
    """
    if inlist[0] > inlist[1]:
        largest = inlist[0]
        second_largest = inlist[1]
    else:
        largest = inlist[1]
        second_largest = inlist[0]
    for item in inlist[2:]:
        if item > largest:
            second_largest = largest
            largest = item
        elif largest > item > second_largest:
            second_largest = item
    return (largest, second_largest)


def one_smallest(inlist):
    """Return the smallest item from the sequence."""
    if len(inlist) == 1:
        return inlist[0]
    if inlist[0] < inlist[1]:
        smallest = inlist[0]
    else:
        smallest = inlist[1]
    for item in inlist[2:]:
        if item < smallest:
            smallest = item
    return smallest


def two_smallest(inlist):
    """Return the two smallest items in the sequence. The sequence must
    contain at least two items.
    """
    if inlist[0] < inlist[1]:
        smallest = inlist[0]
        second_smallest = inlist[1]
    else:
        smallest = inlist[1]
        second_smallest = inlist[0]
    for item in inlist[2:]:
        if item < smallest:
            second_smallest = smallest
            smallest = item
        elif second_smallest < item < smallest:
            second_smallest = item
    return (smallest, second_smallest)


def largest(inlist, n):
    """Return the n largest items in the sequence."""
    pass


def smallest(inlist, n):
    """Return the n smallest items in the sequence."""
    pass


def only_numerics(seq):
    """Return only numerics from the given sequence."""
    seq_type = type(seq)
    return seq_type().join(filter(seq_type.isdigit, seq))


def get_string_index(list_of_strings, string_to_search, start_index=0):
    """Returns the index for the line containing the given string.
    (case-sensitive)
    """
    for idx, line in enumerate(list_of_strings[start_index:]):
        if line.find(string_to_search) > -1:
            return idx
    return -1


def get_regex_index(list_of_strings, regex_to_search, start_index=0):
    """Returns the index for the line matching the given regular
    expression string. (case-sensitive)
    """
    for idx, line in enumerate(list_of_strings[start_index:]):
        if re.search(regex_to_search, line) is not None:
            return idx
    return -1


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
