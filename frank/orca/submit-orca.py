#!/usr/bin/env python2

def pbsfile(inpfile, ppn, time):
    """
    """
    return """#!/bin/bash

#PBS -N {0}
#PBS -q shared
#PBS -l nodes=1:ppn={1}
#PBS -l walltime={2}:00:00
#PBS -j oe
#PBS -l qos=low

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
""".format(inpfile, ppn, time)

def pbsfile_coords(inpfile, ppn, time, xyzfile):
    """
    """
    return """#!/bin/bash

#PBS -N {0}
#PBS -q shared
#PBS -l nodes=1:ppn={1}
#PBS -l walltime={2}:00:00
#PBS -j oe
#PBS -l qos=low

module purge
module load intel/2013.0
module load openmpi/1.6.5-intel12
module load orca/3.0.1

cp $PBS_O_WORKDIR/{0}.in  $LOCAL
cp $PBS_O_WORKDIR/{3}.xyz $LOCAL
cd $LOCAL

run_on_exit() {{
    set -v
    cp $LOCAL/* $PBS_O_WORKDIR
}}

trap run_on_exit EXIT

`which orca` {0}.in >& $PBS_O_WORKDIR/{0}.out
""".format(inpfile, ppn, time, xyzfile)

def pbsfile_ptchrg(inpfile, ppn, time, ptchrgfile):
    """
    """
    return """#!/bin/bash

#PBS -N {0}
#PBS -q shared
#PBS -l nodes=1:ppn={1}
#PBS -l walltime={2}:00:00
#PBS -j oe
#PBS -l qos=low

module purge
module load intel/2013.0
module load openmpi/1.6.5-intel12
module load orca/3.0.1

cp $PBS_O_WORKDIR/{0}.in  $LOCAL
cp $PBS_O_WORKDIR/{3}.xyz $LOCAL
cd $LOCAL

run_on_exit() {{
    set -v
    cp $LOCAL/* $PBS_O_WORKDIR
}}

trap run_on_exit EXIT

`which orca` {0}.in >& $PBS_O_WORKDIR/{0}.out
""".format(inpfile, ppn, time, ptchrgfile)

def pbsfile_coords_ptchrg(inpfile, ppn, time, xyzfile, ptchrgfile):
    """
    """
    return """#!/bin/bash

#PBS -N {0}
#PBS -q shared
#PBS -l nodes=1:ppn={1}
#PBS -l walltime={2}:00:00
#PBS -j oe
#PBS -l qos=low

module purge
module load intel/2013.0
module load openmpi/1.6.5-intel12
module load orca/3.0.1

cp $PBS_O_WORKDIR/{0}.in  $LOCAL
cp $PBS_O_WORKDIR/{3}.xyz $LOCAL
cp $PBS_O_WORKDIR/{4}.xyz $LOCAL
cd $LOCAL

run_on_exit() {{
    set -v
    cp $LOCAL/* $PBS_O_WORKDIR
}}

trap run_on_exit EXIT

`which orca` {0}.in >& $PBS_O_WORKDIR/{0}.out
""".format(inpfile, ppn, time, xyzfile, ptchrgfile)

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
                        default=8,
                        help="number of cores to run on (max 48)")
    parser.add_argument("--time",
                        dest="time",
                        metavar="<time>",
                        type=int,
                        default=144,
                        help="walltime to reserve (max 144 hours)")
    args = parser.parse_args()

    inpfile = args.iname
    xyzfile = args.xname
    ptchrgfile = args.pname

    inpfile = os.path.splitext(inpfile)[0]
    if xyzfile is not None: xyzfile = os.path.splitext(xyzfile)[0]
    if ptchrgfile is not None: ptchrgfile = os.path.splitext(ptchrgfile)[0]

    ppn = args.ppn
    time = args.time

    jobhandle = inpfile + ".pbs"
    jobfile   = open(jobhandle, "w")

    if xyzfile and ptchrgfile:
        print >> jobfile, pbsfile_coords_ptchrg(inpfile, ppn, time, xyzfile, ptchrgfile)
    elif xyzfile:
        print >> jobfile, pbsfile_coords(inpfile, ppn, time, xyzfile)
    elif ptchrgfile:
        print >> jobfile, pbsfile_ptchrg(inpfile, ppn, time, ptchrgfile)
    else:
        print >> jobfile, pbsfile(inpfile, ppn, time)

    jobfile.close()

    subprocess.call(["echo", jobhandle])
    subprocess.call(["qsub", jobhandle])
