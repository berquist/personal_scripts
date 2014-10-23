#!/usr/bin/env python

from __future__ import print_function

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('outputfilename', nargs='+')
    args = parser.parse_args()
    outputfilenames = args.outputfilename

    for outputfilename in outputfilenames:
        with open(outputfilename) as outputfile:
            for line in outputfile:
                if 'g(tot)' in line:
                    print(outputfilename)
                    sline = line.split()
                    g1, g2, g3, giso = float(sline[1]), float(sline[2]), float(sline[3]), float(sline[5])
                    print(' {:<11.8f} {:<11.8f} {:<11.8f} {:<11.8f}'.format(g1, g2, g3, giso))
                    break
