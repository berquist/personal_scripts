#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""read_arma_mat.py: Routines for reading files produced by the
Armadillo C++ template library.
"""

import sys
import numpy as np


def arma_ascii_header_to_dtype(header):

    if 'IS004' in header:
        return np.int32
    else:
        return np.float64


def read_arma_mat_ascii(armaasciifilename):
    """Given a file name, read it in as an ASCII-formatted Armadillo matrix.

    Currently, it supports matrices and cubes.

    The second line of the file contains the dimensions:
    rows, columns, slices (not sure about fields).

    Return a NumPy ndarray of shape [nslices, nrows, ncolumns].
    """

    with open(armaasciifilename) as armafile:
        # The first line contains information about the datatype.
        header = next(armafile)
        dims = next(armafile)
        shape = [int(x) for x in dims.split()]

    dtype = arma_ascii_header_to_dtype(header)

    if len(shape) == 1:
        rows = shape[0]
        columns, slices = 1, 1
    elif len(shape) == 2:
        rows, columns = shape
        slices = 1
    elif len(shape) == 3:
        rows, columns, slices = shape
    else:
        sys.exit(1)

    arma_mat = np.loadtxt(armaasciifilename, skiprows=2, dtype=dtype)

    arma_mat = arma_mat.ravel().reshape((slices, rows, columns))

    if len(shape) == 1:
        pass
    elif len(shape) == 2:
        # Drop the cube slice dimension.
        arma_mat = arma_mat[0]
    elif len(shape) == 3:
        pass

    return arma_mat


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('armaasciifilename',
                        help="""The file name corresponding to the Armadillo object to parse.""")

    parser.add_argument('--print',
                        action='store_true',
                        help="""Print the parsed Armadillo object to stdout.""")
    parser.add_argument('--npz',
                        action='store_true',
                        help="""Should it be re-saved to disk as a NumPy binary file?""")

    args = parser.parse_args()

    arma_mat = read_arma_mat_ascii(args.armaasciifilename)

    if args.print:
        print(arma_mat.shape)
        print(arma_mat)

    if args.npz:
        import os.path
        stub = os.path.splitext(args.armaasciifilename)[0]
        np.savez_compressed(stub + '.npz', arma_mat)
