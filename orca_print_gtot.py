#!/usr/bin/env python

from __future__ import print_function

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('outputfilename', nargs='+')
    parser.add_argument('--pydict', action='store_true')
    args = parser.parse_args()
    outputfilenames = args.outputfilename
    pydict = args.pydict

    t = 'g_1: {:<11.8f} g_2: {:<11.8f} g_3: {:<11.8f} g_para: {:<11.8f} g_perp: {:<11.8f} g_iso: {:<11.8f}'
    t_pydict = "{{'g1': {:<f}, 'g2': {:<f}, 'g3': {:<f}, 'giso': {:<f}, 'gpara': {:<f}, 'gperp': {:<f}}}"

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
                if pydict:
                    print(t_pydict.format(g_1, g_2, g_3, g_iso, g_para, g_perp))
                else:
                    print(t.format(g_1, g_2, g_3, g_para, g_perp, g_iso))
