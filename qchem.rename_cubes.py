#!/usr/bin/env python

'''Rename all Q-Chem cube files in a directory so the number in the middle is the same length (?).

Usage:
  qchem.rename_cubes.py

Options:
  --prefix=PREFIX  Add the given prefix followed by '.' to each filename.
  --print_args     Print the argument block.

'''

from __future__ import print_function


if __name__ == '__main__':

    from docopt import docopt
    import os
    import os.path

    args = docopt(__doc__)

    # Store the maximum length of the internal number.
    maxlen = 0

    # Get the directory contents.
    pwd_contents = os.listdir()

    # Unfortunately, two full traversals need to be performed.
    # 1. Find the maximum length of the internal number and store it.
    for pwd_file in pwd_contents:
        if os.path.splitext(pwd_file)[1] == '.cube':
            newlen = len(pwd_file.split('.')[1])
            if newlen > maxlen:
                maxlen = newlen

    # prefix = args['--prefix'] + '.'

    # 2. Go through each cube file again and rename if necessary.
    for pwd_file in pwd_contents:
        if os.path.splitext(pwd_file)[1] == '.cube':
            splitname = pwd_file.split('.')
            filenumlen = len(splitname[1])
            ### Should do the prefix operation on this line here?
            if filenumlen < maxlen:
                numzeros = maxlen - filenumlen
                splitname[1] = ('0' * numzeros) + splitname[1]
                newfilename = '.'.join(splitname)
                os.rename(pwd_file, newfilename)
                print(pwd_file + ' -> ' + newfilename)
