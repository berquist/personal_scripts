#!/usr/bin/env python

from __future__ import print_function
from __future__ import division

import numpy as np

from cclib.io import ccopen


def getargs():
    import argparse
    parser = argparse.ArgumentParser()
    arg = parser.add_argument
    arg('outputfile', nargs='*')
    arg('--only-iso', action='store_true')
    args = parser.parse_args()
    return args

if __name__ == '__main__':

    args = getargs()

    for outputfilename in args.outputfile:
        job = ccopen(outputfilename)
        try:
            data = job.parse()
            if hasattr(data, 'polarizabilities'):
                print(outputfilename)
                for polarizability in data.polarizabilities:
                    if not args.only_iso:
                        print(polarizability)
                    print('avg(trace)       :', np.trace(polarizability) / 3)
                    print('avg(sum(eigvals)):', np.sum(np.linalg.eigvals(polarizability)) / 3)
        except:
            pass
