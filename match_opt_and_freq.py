#!/usr/bin/env python

"""match_opt_and_freq.py: Given ..."""

from __future__ import print_function

import os
import re


def getargs():

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--dir-opt', default='.')
    parser.add_argument('--dir-freq', default='.')

    parser.add_argument('--print-opt-outputs-missing-freq-outputs',
                        action='store_true',
                        help="""useful for direct input into `qchem_make_freq_input_from_opt.py`""")
    parser.add_argument('--print-opt-outputs-missing-freq-inputs',
                        action='store_true',
                        help="""useful for direct input into `qchem_make_freq_input_from_opt.py`""")

    args = parser.parse_args()

    return args


if __name__ == '__main__':

    args = getargs()

    dir_opt = os.path.abspath(args.dir_opt)
    dir_freq = os.path.abspath(args.dir_freq)

    inputs_opt = [os.path.basename(f) for f in os.listdir(path=dir_opt)
                  if f.endswith(".in") and "opt" in os.path.basename(f)]
    inputs_freq = [os.path.basename(f) for f in os.listdir(path=dir_freq)
                   if f.endswith(".in") and "freq" in os.path.basename(f)]
    outputs_opt = [os.path.basename(f) for f in os.listdir(path=dir_opt)
                   if f.endswith(".out") and "opt" in os.path.basename(f)]
    outputs_freq = [os.path.basename(f) for f in os.listdir(path=dir_freq)
                    if f.endswith(".out") and "freq" in os.path.basename(f)]

    for output_opt in outputs_opt:
        output_opt_bn = os.path.basename(output_opt)
        opt_repl_freq = re.sub('opt\d*', 'freq', output_opt_bn)
        if args.print_opt_outputs_missing_freq_outputs:
            if opt_repl_freq not in outputs_freq:
                print(output_opt_bn)
        if args.print_opt_outputs_missing_freq_inputs:
            if opt_repl_freq.replace(".out", ".in") not in inputs_freq:
                print(output_opt_bn)
