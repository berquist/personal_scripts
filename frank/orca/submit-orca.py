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
#PBS -m abe
#PBS -M ${{USER}}@pitt.edu}

module purge
module load intel/2013.0
module load openmpi/1.6.5-intel12
module load orca/3.0.1

cp $PBS_O_WORKDIR/{0}.in  $LOCAL
cd $LOCAL

run_on_exit() {{
    set -v
    cp $LOCAL/* $PBS_O_WORKDIR
}}

trap run_on_exit EXIT

`which orca` {0}.in >& $PBS_O_WORKDIR/{0}.out
""".format(inpfile, ppn, time, queue)

def pbsfile_coords(inpfile, ppn, time, queue, xyzfile):
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
module load openmpi/1.6.5-intel12
module load orca/3.0.1

cp $PBS_O_WORKDIR/{0}.in  $LOCAL
cp $PBS_O_WORKDIR/{4}.xyz $LOCAL
cd $LOCAL

run_on_exit() {{
    set -v
    cp $LOCAL/* $PBS_O_WORKDIR
}}

trap run_on_exit EXIT

`which orca` {0}.in >& $PBS_O_WORKDIR/{0}.out
""".format(inpfile, ppn, time, queue, xyzfile)

def pbsfile_ptchrg(inpfile, ppn, time, queue, ptchrgfile):
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
module load openmpi/1.6.5-intel12
module load orca/3.0.1

cp $PBS_O_WORKDIR/{0}.in  $LOCAL
cp $PBS_O_WORKDIR/{4}.xyz $LOCAL
cd $LOCAL

run_on_exit() {{
    set -v
    cp $LOCAL/* $PBS_O_WORKDIR
}}

trap run_on_exit EXIT

`which orca` {0}.in >& $PBS_O_WORKDIR/{0}.out
""".format(inpfile, ppn, time, queue, ptchrgfile)

def pbsfile_coords_ptchrg(inpfile, ppn, time, queue, xyzfile, ptchrgfile):
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
module load openmpi/1.6.5-intel12
module load orca/3.0.1

cp $PBS_O_WORKDIR/{0}.in  $LOCAL
cp $PBS_O_WORKDIR/{4}.xyz $LOCAL
cp $PBS_O_WORKDIR/{5}.xyz $LOCAL
cd $LOCAL

run_on_exit() {{
    set -v
    cp $LOCAL/* $PBS_O_WORKDIR
}}

trap run_on_exit EXIT

`which orca` {0}.in >& $PBS_O_WORKDIR/{0}.out
""".format(inpfile, ppn, time, queue, xyzfile, ptchrgfile)

if __name__ == "__main__":
    import argparse
    import os.path
    import subprocess

    parser = argparse.ArgumentParser(description="")
    parser.add_argument(dest="iname",
                        metavar="<inpfile>",
                        type=str,
                        help="the ORCA input file to submit")
    parser.add_argument("--xyzfile",
                        dest="xname",
                        metavar="<xyzfile>",
                        type=str,
                        default=None,
                        help="XYZ file containing molecular coordinates")
    parser.add_argument("--ptchrgfile",
                        dest="pname",
                        metavar="<ptchrgfile>",
                        type=str,
                        default=None,
                        help="XYZ file containing point charges (element as charge magnitude)")
    parser.add_argument("--ppn",
                        dest="ppn",
                        metavar="<ppn>",
                        type=int,
                        default=4,
                        help="number of cores to run on (max shared=48, shared_large=16)")
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

    inpfile = args.iname
    xyzfile = args.xname
    ptchrgfile = args.pname

    inpfile = os.path.splitext(inpfile)[0]
    if xyzfile is not None: xyzfile = os.path.splitext(xyzfile)[0]
    if ptchrgfile is not None: ptchrgfile = os.path.splitext(ptchrgfile)[0]

    ppn = args.ppn
    time = args.time
    queue = args.queue

    jobhandle = inpfile + ".pbs"
    jobfile   = open(jobhandle, "w")

    if xyzfile and ptchrgfile:
        print >> jobfile, pbsfile_coords_ptchrg(inpfile, ppn, time, queue, xyzfile, ptchrgfile)
    elif xyzfile:
        print >> jobfile, pbsfile_coords(inpfile, ppn, time, queue, xyzfile)
    elif ptchrgfile:
        print >> jobfile, pbsfile_ptchrg(inpfile, ppn, time, queue, ptchrgfile)
    else:
        print >> jobfile, pbsfile(inpfile, ppn, time, queue)

    jobfile.close()

    subprocess.call(["echo", jobhandle])
    # call manually: 'find . -name "*pbs" -exec qsub '{}' \;'
    # subprocess.call(["qsub", jobhandle])
