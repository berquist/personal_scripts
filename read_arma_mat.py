"""read_arma_mat.py: Routines for reading files produced by the
Armadillo C++ template library.
"""

from __future__ import print_function

import numpy as np


def read_arma_mat_ascii(armaasciifilename):
    """Given a file name, read it in as an ASCII-formatted Armadillo matrix.

    Currently, it supports matrices and cubes.

    # the second line of the file contains the dimensions:
    # rows, columns, slices (not sure about fields)
    """

    with open(armaasciifilename) as armafile:
        next(armafile)
        shape = list(map(int, next(armafile).split()))

    if len(shape) == 2:
        rows, columns = shape
        slices = 0
    if len(shape) == 3:
        rows, columns, slices = shape

    arma_mat = np.loadtxt(armaasciifilename, skiprows=2)

    arma_mat = arma_mat.ravel().reshape((slices, rows, columns))

    return arma_mat


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('armaasciifilename',
                        help="""The file name corresponding to the Armadillo object to parse.""")
    parser.add_argument('--npdisk',
                        action='store_true',
                        help="""Should it be re-saved to disk as a NumPy binary file?""")

    args = parser.parse_args()

    arma_mat = read_arma_mat_ascii(args.armaasciifilename)

    if args.npdisk:
        np.save(arma_mat)
