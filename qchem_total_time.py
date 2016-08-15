#!/usr/bin/env python

from __future__ import division
from __future__ import print_function

import numpy as np
np_formatter = {
    'float_kind': lambda x: '{:14.8f}'.format(x)
}
np.set_printoptions(linewidth=200, formatter=np_formatter)

def qchem_get_total_times(outputfilename):
    time_wall, time_cpu = None, None
    with open(outputfilename) as fh:
        for line in fh:
            if 'Total job time' in line:
                tokens = line.split()
                time_wall_str, time_cpu_str = tokens[3], tokens[4]
                time_wall = float(time_wall_str[:-8])
                time_cpu = float(time_cpu_str[:-6])
    return time_wall, time_cpu

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('outputfile', nargs='+')

    args = parser.parse_args()

    times_wall = []
    times_cpu = []

    for outputfilename in args.outputfile:
        time_wall, time_cpu = qchem_get_total_times(outputfilename)
        if time_wall:
            times_wall.append(time_wall)
        if time_cpu:
            times_cpu.append(time_cpu)

    times_seconds = np.array(sorted(zip(times_wall, times_cpu)))
    times_hours = times_seconds / 3600.0
    times_hours_wall = times_hours[:, 0]
    times_hours_cpu = times_hours[:, 1]
    speedup = times_hours_cpu / times_hours_wall
    print(times_hours)
    print(speedup)
    mmin, mmax = min(times_hours_wall), max(times_hours_wall)
    rng = mmax - mmin
    print(mmin, mmax, rng)
    print('mean +/- stdev: {:f} +/- {:f}'.format(np.mean(times_hours_wall), np.std(times_hours_wall)))
