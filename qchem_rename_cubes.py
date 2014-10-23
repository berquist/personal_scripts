#!/usr/bin/env python

'''Rename all Q-Chem cube files in a directory so the number in the middle is the same length (?).

Usage:
  qchem.rename_cubes.py

Options:
  --print_args     Print the argument block.

'''

from __future__ import print_function


def pad_zeros(num, maxlen):
    '''
    Pad the given number with zeros to left until the total length is maxlen.
    '''
    numstr = str(num)
    numlen = len(numstr)
    if numlen < maxlen:
        numzeros = maxlen - numlen
        padnum = (numzeros * '0') + numstr
        return padnum
    else:
        return numstr


if __name__ == '__main__':

    from docopt import docopt
    from glob import glob
    import os
    import os.path

    args = docopt(__doc__)

    # Store the maximum length of the internal number.
    maxlen = 0

    # Get the directory contents.
    pwd_contents = glob('*.cube')

    # Unfortunately, two full traversals need to be performed.
    # 1. Find the maximum length of the internal number and store it.
    for pwd_file in pwd_contents:
        newlen = len(pwd_file.split('.')[1])
        if newlen > maxlen:
            maxlen = newlen

    # 2. Go through each cube file again and rename if necessary.
    for pwd_file in pwd_contents:
        splitname = pwd_file.split('.')
        filenumlen = len(splitname[1])
        if filenumlen < maxlen:
            splitname[1] = pad_zeros(splitname[1], maxlen)
            newfilename = '.'.join(splitname)
            os.rename(pwd_file, newfilename)
            print(pwd_file + ' -> ' + newfilename)
