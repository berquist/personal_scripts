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
            match = False
            for line in outputfile:
                # single-reference calculations
                if 'g(tot)' in line:
                    print(outputfilename)
                    sline = line.split()
                    match = True
                    g_1, g_2, g_3, g_iso = float(sline[1]), float(sline[2]), float(sline[3]), float(sline[5])
                    break
                # multi-reference calculations
                if 'g-factors:' in line:
                    print(outputfilename)
                    line = next(outputfile)
                    sline = line.split()
                    match = True
                    g_1, g_2, g_3, g_iso = float(sline[0]), float(sline[1]), float(sline[2]), float(sline[-1])
                    break
            if match:
                g_perp = (g_1 + g_2) / 2
                g_para = g_3
                print(' {:<11.8f} {:<11.8f} {:<11.8f}'.format(g_1, g_2, g_3))
                print(' g_para: {:<11.8f} g_perp: {:<11.8f} g_iso: {:<11.8f}'.format(g_para, g_perp, g_iso))
