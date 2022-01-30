#!/usr/bin/env python

""""""


from cclib.io import ccopen


def get_job_data(filename):
    """"""
    job = ccopen(filename)
    data = job.parse()
    return data


def get_copper_idx(data):
    """"""
    return list(data.atomnos).index(29)


def get_spin_densities(data, idx):
    """"""
    spin_densities = dict()
    for partitioning in data.atomspins.keys():
        spin_idx = data.atomspins[partitioning][idx]
        spin_total = sum(data.atomspins[partitioning])
        spin_densities[partitioning] = dict()
        spin_densities[partitioning][idx] = spin_idx
        spin_densities[partitioning]['total'] = spin_total
        spin_densities[partitioning]['density'] = (spin_idx / spin_total) * 100
    return spin_densities


def main(filename):
    """"""
    data = get_job_data(filename)
    idx = get_copper_idx(data)
    spin_densities = get_spin_densities(data, idx)
    print('=' * 78)
    print(filename)
    for partitioning in spin_densities.keys():
        print(' {}'.format(partitioning))
        print('  center {:3d}: {:f}'.format(idx, spin_densities[partitioning][idx]))
        print('       total: {:f}'.format(spin_densities[partitioning]['total']))
        print('     density: {:f}'.format(spin_densities[partitioning]['density']))
    print('=' * 78)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('compchemlogfile', nargs='+')

    args = parser.parse_args()

    filenames = args.compchemlogfile

    for filename in filenames:
        main(filename)
