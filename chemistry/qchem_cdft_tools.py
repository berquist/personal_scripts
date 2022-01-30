from utils import make_file_iterator

import numpy as np
from cclib.io import ccopen


def test_parse_cdft_block():
    filename = "paper1_MMIM+_CO2_TfO-.out"
    cdft_becke_populations = extract_cdft_becke_populations(filename).tolist()
    constraint_values, all_constraints = parse_cdft_block(filename)
    assert len(constraint_values) == 1
    assert len(all_constraints) == 1
    assert len(all_constraints[0]) == 2
    charges_cation = [
        -0.632940,
        -0.022999,
        -0.021328,
        0.550942,
        -0.542662,
        -0.540571,
        0.435049,
        0.436665,
        -1.368487,
        0.429684,
        0.422761,
        0.454923,
        -1.367766,
        0.455151,
        0.427207,
        0.425454,
    ]
    charges_anion = [
        -1.931365,
        0.763746,
        0.743214,
        0.707769,
        -0.300801,
        0.183607,
        0.191789,
        0.183127,
    ]
    charges_remainder = [-0.442606, 0.181832, 0.179663]
    idx_cation_1 = all_constraints[0][0][1] - 1
    idx_cation_2 = all_constraints[0][0][2] - 1
    idx_anion_1 = all_constraints[0][1][1] - 1
    idx_anion_2 = all_constraints[0][1][2] - 1
    parsed_charges_cation = cdft_becke_populations[idx_cation_1 : idx_cation_2 + 1]
    parsed_charges_anion = cdft_becke_populations[idx_anion_1 : idx_anion_2 + 1]
    parsed_charges_remainder = cdft_becke_populations[idx_anion_2 + 1 :]
    assert parsed_charges_cation == charges_cation
    assert parsed_charges_anion == charges_anion
    assert parsed_charges_remainder == charges_remainder
    charge_cation = sum(charges_cation)
    charge_anion = sum(charges_anion)
    charge_remainder = sum(charges_remainder)
    # print(charge_cation, charge_anion, charge_remainder, charge_cation
    #       + charge_anion + charge_remainder)
    return


def extract_cdft_becke_populations(outputfilename):

    cdft_becke_populations = []

    fi = make_file_iterator(outputfilename)

    line = ""
    while line.strip() != "CDFT Becke Populations":
        line = next(fi)
    line = next(fi)
    assert list(set(line.strip())) == ["-"]
    line = next(fi)
    assert line.strip() == "Atom  Net Number"
    line = next(fi)
    while list(set(line.strip())) != ["-"]:
        idx, atomsymbol, pop = line.split()
        pop = float(pop)
        cdft_becke_populations.append(pop)
        line = next(fi)

    return np.array(cdft_becke_populations)


def parse_cdft_block(outputfilename):

    constraint_values = []
    all_constraints = []
    constraints = []

    fi = make_file_iterator(outputfilename)

    line = ""
    while line.strip().lower() != "$cdft":
        line = next(fi)
    line = next(fi)
    while line.strip().lower() != "$end":

        tokens = [int(x) for x in line.split()]

        if len(tokens) == 0:
            pass
        # constraint value
        elif len(tokens) == 1:
            constraint_values.append(tokens[0])
            # there are a new set of constraints for every average constraint value
            all_constraints.append(constraints)
            constraints = []
        # doesn't make sense
        elif len(tokens) == 2:
            pass
        # charge constraint
        elif len(tokens) == 3:
            constraints.append(tokens)
        # spin constraint
        elif len(tokens) == 4:
            assert tokens[2].lower() == "s"
            pass
        # 5 or more doesn't make sense
        else:
            pass
        line = next(fi)

    del all_constraints[0]
    all_constraints.append(constraints)

    return constraint_values, all_constraints


if __name__ == "__main__":

    # test_parse_cdft_block()

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("outputfilename", nargs="*")

    args = parser.parse_args()

    for outputfilename in args.outputfilename:

        print("=" * 70)
        print(outputfilename)

        # job = ccopen(outputfilename)
        # data = job.parse()
        # atomnos = data.atomnos

        cdft_becke_populations = extract_cdft_becke_populations(outputfilename)

        # assert len(cdft_becke_populations) == len(atomnos)

        print(cdft_becke_populations)
        total = sum(cdft_becke_populations)
        print("total:", total)

        constraint_values, all_constraints = parse_cdft_block(outputfilename)
        assert len(constraint_values) == len(all_constraints)

        for constraints_for_coeff_list in all_constraints:
            population_remainder = total
            for constraint in constraints_for_coeff_list:
                charge_deviation, idx_atom1, idx_atom2 = constraint
                idx_atom1 -= 1
                idx_atom2 -= 1
                constraint_total_pop = sum(cdft_becke_populations[idx_atom1 : idx_atom2 + 1])
                print("constraint:", constraint, constraint_total_pop)
                population_remainder -= constraint_total_pop
            # What is the population of the remainder?
            # This is wrong; what if not all atoms had a constraint?
            # It would miss them.
            populations_remainder = cdft_becke_populations[idx_atom2 + 1 :]
            # print('remainder:', sum(populations_remainder))
            print("remainder:", population_remainder)
