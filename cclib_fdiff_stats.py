#!/usr/bin/env python

import re

import numpy as np

from cclib.io import ccread


re_time_scf = re.compile('^ SCF time:\s*CPU (\d*\.\d*)s\s*wall\s(\d*\.\d*)s')
re_time_grad = re.compile('^ Gradient time:\s*CPU (\d*\.\d*) s\s*wall\s(\d*\.\d*) s')

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('outputfile', nargs='*')
    args = parser.parse_args()
    outputfiles = args.outputfile

    for outputfilename in outputfiles:

        times_scf_cpu = []
        times_scf_wall = []
        times_grad_cpu = []
        times_grad_wall = []

        with open(outputfilename) as outputfile:
            for line in outputfile:
                matches_scf = re_time_scf.findall(line)
                if matches_scf:
                    time_scf_cpu, time_scf_wall = [float(time) for time in matches_scf[0]]
                    times_scf_cpu.append(time_scf_cpu)
                    times_scf_wall.append(time_scf_wall)
                matches_grad = re_time_grad.findall(line)
                if matches_grad:
                    time_grad_cpu, time_grad_wall = [float(time) for time in matches_grad[0]]
                    times_grad_cpu.append(time_grad_cpu)
                    times_grad_wall.append(time_grad_wall)

        times_scf = np.array([times_scf_cpu, times_scf_wall])
        times_grad = np.array([times_grad_cpu, times_grad_wall])

        couldnt_parse = False
        try:
            data = ccread(outputfilename)
            natom = data.natom
            nsteps = (6 * natom) + 1
            nsteps_current = times_grad.shape[1]
            pct = 100 * (nsteps_current / nsteps)
        except StopIteration:
            couldnt_parse = True
            nsteps = -1
            nsteps_current = -1
            pct = -1
        nsteps_remaining = nsteps - nsteps_current

        print('=' * 78)
        print(outputfilename)
        print('-' * 78)
        if couldnt_parse:
            print(" couldn't parse with cclib due to StopIteration")
        else:
            print(' progress: {:d}/{:d} -> {:.2f}%'.format(nsteps_current, nsteps, pct))

        times_scf /= 3600
        times_grad /= 3600
        # times = times_scf + times_grad

        tot_time_scf = np.sum(times_scf, axis=1)
        avg_time_scf = np.mean(times_scf, axis=1)
        std_time_scf = np.std(times_scf, axis=1)
        print(' SCF count, totals, averages, standard deviations')
        print(times_scf.shape[1])
        print(tot_time_scf)
        print(avg_time_scf)
        print(std_time_scf)

        tot_time_grad = np.sum(times_grad, axis=1)
        avg_time_grad = np.mean(times_grad, axis=1)
        std_time_grad = np.std(times_grad, axis=1)
        print(' Gradient count, totals, averages, standard deviations')
        print(times_grad.shape[1])
        print(tot_time_grad)
        print(avg_time_grad)
        print(std_time_grad)

        tot_time = tot_time_scf + tot_time_grad
        avg_time = avg_time_scf + avg_time_grad
        print(' Total time')
        print(tot_time)
        print(' Average time per step')
        print(avg_time)

        print(' Remaining time')
        print(avg_time * nsteps_remaining)
