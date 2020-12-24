#!/usr/bin/env python



def read_binary(binaryfilename):
    """Return the bytes present in the given binary file name.
    """

    with open(binaryfilename, 'rb') as binaryfile:
        readbytes = binaryfile.read()

    return readbytes

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('binaryfilename')

    args = parser.parse_args()

    binaryfile = read_binary(args.binaryfilename)
    print(binaryfile)
