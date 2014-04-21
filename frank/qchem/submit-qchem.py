#!/usr/bin/env python2

def pbsfile(inpfile, ppn, time, queue):
    """
    """
    return """#!/bin/bash

#PBS -N {0}
#PBS -q {3}
#PBS -l nodes=1:ppn={1}
#PBS -l walltime={2}:00:00
#PBS -j oe
#PBS -l qos=low

module purge
module load intel/2013.0
module load qchem/dlambrecht/4.1-trunk.20130919.omp.ccman2

cp $PBS_O_WORKDIR/{0}.qcin  $LOCAL
cd $LOCAL

run_on_exit() {{
    set -v
    cp $LOCAL/* $PBS_O_WORKDIR
}}

trap run_on_exit EXIT

`which qchem` -nt {1} {0}.qcin >& $PBS_O_WORKDIR/{0}.qcout
""".format(inpfile, ppn, time, queue)

if __name__ == "__main__":
    import argparse
    import os.path
    import subprocess

    parser = argparse.ArgumentParser(description="")
    parser.add_argument(dest="iname",
                        metavar="<inpfile>",
                        type=str,
                        help="the Q-Chem input file to submit")
    parser.add_argument("--ppn",
                        dest="ppn",
                        metavar="<ppn>",
                        type=int,
                        default=4,
                        help="number of cores to run on (max shared=48, shared_large=16")
    parser.add_argument("--time",
                        dest="time",
                        metavar="<time>",
                        type=int,
                        default=96,
                        help="walltime to reserve (max 144 hours)")
    parser.add_argument("--queue",
                        dest="queue",
                        metavar="<queue>",
                        type=str,
                        default="shared",
                        help="queue to run in (typically shared or shared_large")
    args = parser.parse_args()
    inpfile = os.path.splitext(args.iname)[0]
    ppn = args.ppn
    time = args.time
    queue = args.queue

    jobhandle = inpfile + ".pbs"
    jobfile   = open(jobhandle, "w")

    print >> jobfile, pbsfile(inpfile, ppn, time, queue)

    jobfile.close()

    subprocess.call(["echo", jobhandle])
    # call manually: 'find . -name "*pbs" -exec qsub '{}' \;'
    # subprocess.call(["qsub", jobhandle])
