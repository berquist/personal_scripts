#!/usr/bin/env python

"""cclib_plot_scf_convergence.py: Given a computational chemistry
logfile for ...
"""


import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

import argparse
import os.path

import cclib
from cclib.io import ccopen
from cclib.parser import utils


def main():
    """The main routine!"""

    parser = argparse.ArgumentParser()

    parser.add_argument("compchemfilename", nargs="+")

    args = parser.parse_args()
    compchemfilenames = args.compchemfilename

    for compchemfilename in compchemfilenames:

        stub = os.path.splitext(compchemfilename)[0]

        job = ccopen(compchemfilename)
        data = job.parse()

        fig, ax = plt.subplots()

        if type(job) == cclib.parser.qchemparser.QChem:

            scfenergies = [
                utils.convertor(scfenergy, "eV", "hartree") for scfenergy in data.scfenergies
            ]
            print(scfenergies)
            # scfenergies = [scfenergy for scfenergy in data.scfenergies]

            steps = range(1, len(scfenergies) + 1)

            ax.plot(steps, scfenergies, label="SCF energy")

            ax.set_title(stub)
            ax.set_xlabel("SCF step #")
            ax.set_xticks(steps)

        elif type(job) == cclib.parser.orcaparser.ORCA:

            pass

        else:
            pass

        ax.legend(loc="best", fancybox=True)

        fig.savefig(stub + ".pdf", bbox_inches="tight")


if __name__ == "__main__":
    main()
