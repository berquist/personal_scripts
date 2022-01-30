#!/usr/bin/env python

"""match_opt_and_freq.py: Given ..."""


import os
import re


def getargs():

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--debug-big", action="store_true")

    parser.add_argument("--dir-opt", default=".")
    parser.add_argument("--dir-freq", default=".")

    parser.add_argument(
        "--print-opt-outputs-missing-freq-outputs",
        action="store_true",
        help="""useful for direct input into `qchem_make_freq_input_from_opt.py`""",
    )
    parser.add_argument(
        "--print-opt-outputs-missing-freq-inputs",
        action="store_true",
        help="""useful for direct input into `qchem_make_freq_input_from_opt.py`""",
    )

    args = parser.parse_args()

    return args


def pprint(l, header):
    print("========== {}: ==========".format(header))
    for x in l:
        print(x)
    return


def get_files_from_path(path, ext=".out"):
    matchfiles = []
    # Walk the directory tree to find all potential output files.
    for (root, dirs, files) in os.walk(path):
        for f in files:
            if f.endswith(ext):
                matchfiles.append(os.path.join(root, f))
    return sorted(matchfiles)


if __name__ == "__main__":

    import sys

    args = getargs()

    dir_opt = os.path.abspath(args.dir_opt)
    dir_freq = os.path.abspath(args.dir_freq)

    if args.debug:
        print("dir_opt : {}".format(dir_opt), file=sys.stderr)
        print("dir_freq: {}".format(dir_freq), file=sys.stderr)

    inputs_opt = [
        f for f in get_files_from_path(dir_opt, ext=".in") if "opt" in os.path.basename(f)
    ]
    inputs_freq = [
        f for f in get_files_from_path(dir_freq, ext=".in") if "freq" in os.path.basename(f)
    ]
    outputs_opt = [
        f for f in get_files_from_path(dir_opt, ext=".out") if "opt" in os.path.basename(f)
    ]
    outputs_freq = [
        f for f in get_files_from_path(dir_freq, ext=".out") if "freq" in os.path.basename(f)
    ]

    if args.debug_big:
        pprint(inputs_opt, "inputs_opt")
        pprint(inputs_freq, "inputs_freq")
        pprint(outputs_opt, "outputs_opt")
        pprint(outputs_freq, "outputs_freq")

    # Master loop over all completed geometry optimization output
    # files.
    for output_opt in outputs_opt:
        opt_repl_freq = os.path.basename(re.sub("opt\d*", "freq", output_opt))
        if args.print_opt_outputs_missing_freq_outputs:
            if opt_repl_freq not in outputs_freq:
                print(os.path.relpath(output_opt))
        if args.print_opt_outputs_missing_freq_inputs:
            if opt_repl_freq.replace(".out", ".in") not in inputs_freq:
                print(os.path.relpath(output_opt))
