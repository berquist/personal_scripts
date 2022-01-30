#!/usr/bin/env python


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("outputfilename", nargs="+")
    parser.add_argument("--pydict", action="store_true")
    parser.add_argument("--write", default="print", choices=("print", "pyfile", "txtfile"))
    parser.add_argument("--pyfilename", default="gtot.py")
    args = parser.parse_args()
    outputfilenames = args.outputfilename

    t = "g_1: {:<11.8f} g_2: {:<11.8f} g_3: {:<11.8f} g_para: {:<11.8f} g_perp: {:<11.8f} g_iso: {:<11.8f}"
    t_pydict = (
        "{{'g1': {:<f}, 'g2': {:<f}, 'g3': {:<f}, 'giso': {:<f}, 'gpara': {:<f}, 'gperp': {:<f}}}"
    )

    results = dict()

    for outputfilename in outputfilenames:
        with open(outputfilename) as outputfile:
            match = False
            for line in outputfile:
                # single-reference calculations
                if "g(tot)" in line:
                    print(outputfilename)
                    sline = line.split()
                    match = True
                    g_1, g_2, g_3, g_iso = (
                        float(sline[1]),
                        float(sline[2]),
                        float(sline[3]),
                        float(sline[5]),
                    )
                    results[outputfilename] = dict()
                    results[outputfilename]["g1"] = g_1
                    results[outputfilename]["g2"] = g_2
                    results[outputfilename]["g3"] = g_3
                    results[outputfilename]["giso"] = g_iso
                    break
                # multi-reference calculations
                if "g-factors:" in line:
                    print(outputfilename)
                    line = next(outputfile)
                    sline = line.split()
                    match = True
                    g_1, g_2, g_3, g_iso = (
                        float(sline[0]),
                        float(sline[1]),
                        float(sline[2]),
                        float(sline[-1]),
                    )
                    results[outputfilename] = dict()
                    results[outputfilename]["g1"] = g_1
                    results[outputfilename]["g2"] = g_2
                    results[outputfilename]["g3"] = g_3
                    results[outputfilename]["giso"] = g_iso
                    break
            if match:
                g_perp = (g_1 + g_2) / 2
                g_para = g_3
                if args.pydict:
                    print(t_pydict.format(g_1, g_2, g_3, g_iso, g_para, g_perp))
                else:
                    print(t.format(g_1, g_2, g_3, g_para, g_perp, g_iso))

    if args.write == "pyfile":
        with open(args.pyfilename, "w") as f:
            print("results =", results, file=f)
