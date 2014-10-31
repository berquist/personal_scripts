#!/usr/bin/env python

from __future__ import print_function

if __name__ == '__main__':

    import argparse
    import os.path
    import numpy as np

    parser = argparse.ArgumentParser()
    parser.add_argument('outputfilename', nargs='+')
    args = parser.parse_args()
    outputfilenames = args.outputfilename

    for outputfilename in outputfilenames:
        with open(outputfilename) as outputfile:
            for line in outputfile:
                # matches if we are doing a perturbative calculation
                if 'TOTAL EPR Delta g-matrix (ppt)' in line:
                    print(os.path.abspath(outputfilename))
                    while 'Principal components' not in line:
                        line = next(outputfile)
                    next(outputfile)
                    line = next(outputfile)
                    gprin_ppt = np.array(map(float, line.split()))
                    gprin_full = (gprin_ppt / 1000) + 2.002319
                    print('  ppt: {:>11.3f} {:>11.3f} {:>11.3f}'.format(*gprin_ppt))
                    print(' full: {:>11.3f} {:>11.3f} {:>11.3f}'.format(*gprin_full))
                    break
                # matches if we are doing a self-consistent calculation
                if 'Principal g-values' in line:
                    print(os.path.abspath(outputfilename))
                    gprin_full = np.array(map(float, line.split()[2:]))
                    line = next(outputfile)
                    gprin_ppt = np.array(map(float, line.split()[1:])) * 1000
                    print('  ppt: {:>11.3f} {:>11.3f} {:>11.3f}'.format(*gprin_ppt))
                    print(' full: {:>11.3f} {:>11.3f} {:>11.3f}'.format(*gprin_full))
                    break
