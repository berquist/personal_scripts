#!/usr/bin/env python

from __future__ import print_function

from scripts.utils import make_file_iterator


def getargs():

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("outputfilename", nargs="+")

    args = parser.parse_args()

    return args


def main(args):

    hartree_to_ev = 27.211386

    for outputfilename in args.outputfilename:

        print(outputfilename)

        fi = make_file_iterator(outputfilename)

        minima_energies_hartree = []
        minima_distances = []

        for line in fi:
            # This needs more work...
            if "EDistance" in line:
                edistance = float(line[10:])
                line = next(fi)
                distance = float(line[9:])
                minima_distances.append((edistance, distance))
            if "Writing energy" in line:
                minimum_energy_hartree = float(line.split()[3])
                minima_energies_hartree.append(minimum_energy_hartree)

        if len(minima_energies_hartree) > 0:
            minima_energies_ev = [(e*hartree_to_ev) for e in minima_energies_hartree]

            global_minimum_energy_hartree = minima_energies_hartree[0]
            global_minimum_energy_ev = minima_energies_ev[0]
            relative_energies_hartree = sorted([(e - global_minimum_energy_hartree)
                                                for e in minima_energies_hartree[1:]])
            relative_energies_ev = sorted([(e - global_minimum_energy_ev)
                                           for e in minima_energies_ev[1:]])

            state_gap_energies_hartree = []
            for i, et in enumerate(relative_energies_hartree):
                if i > 0:
                    eb = relative_energies_hartree[i - 1]
                    state_gap_energies_hartree.append(et - eb)
            state_gap_energies_ev = []
            for i, et in enumerate(relative_energies_ev):
                if i > 0:
                    eb = relative_energies_ev[i - 1]
                    state_gap_energies_ev.append(et - eb)

            print(" E(minimum) - E(GS) (eV)")
            for relative_energy_ev in relative_energies_ev:
                print(" {:7.5f}".format(relative_energy_ev))
            print(" Gap between minima")
            for state_gap_energy_ev in state_gap_energies_ev:
                print(" {:7.5f}".format(state_gap_energy_ev))


    return locals()

if __name__ == "__main__":
    args = getargs()
    main_locals = main(args)
