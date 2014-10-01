#!/usr/bin/env python2

def template_pbsfile(inpfile, ppn, time, queue):
    return """#!/bin/bash

#PBS -N {0}
#PBS -q {3}
#PBS -l nodes=1:ppn={1}
#PBS -l walltime={2}:00:00
#PBS -j oe
#PBS -l qos=low
#PBS -m abe
#PBS -M {username}@pitt.edu

module purge
module load orca/3.0.2

cp $PBS_O_WORKDIR/{0}.in  $LOCAL
cd $LOCAL

run_on_exit() {{
    set -v
    cp $LOCAL/* $PBS_O_WORKDIR
}}

trap run_on_exit EXIT

`which orca` {0}.in >& $PBS_O_WORKDIR/{0}.out
""".format(inpfile, ppn, time, queue, username=os.environ['USER'])

def template_pbsfile_coords(inpfile, ppn, time, queue, xyzfile):
    return """#!/bin/bash

#PBS -N {0}
#PBS -q {3}
#PBS -l nodes=1:ppn={1}
#PBS -l walltime={2}:00:00
#PBS -j oe
#PBS -l qos=low
#PBS -m abe
#PBS -M {username}@pitt.edu

module purge
module load orca/3.0.2

cp $PBS_O_WORKDIR/{0}.in  $LOCAL
cp $PBS_O_WORKDIR/{4}.xyz $LOCAL
cd $LOCAL

run_on_exit() {{
    set -v
    cp $LOCAL/* $PBS_O_WORKDIR
}}

trap run_on_exit EXIT

`which orca` {0}.in >& $PBS_O_WORKDIR/{0}.out
""".format(inpfile, ppn, time, queue, xyzfile, username = os.environ['USER'])

def template_pbsfile_ptchrg(inpfile, ppn, time, queue, ptchrgfile):
    return """#!/bin/bash

#PBS -N {0}
#PBS -q {3}
#PBS -l nodes=1:ppn={1}
#PBS -l walltime={2}:00:00
#PBS -j oe
#PBS -l qos=low
#PBS -m abe
#PBS -M {username}@pitt.edu

module purge
module load orca/3.0.2

cp $PBS_O_WORKDIR/{0}.in  $LOCAL
cp $PBS_O_WORKDIR/{4}.xyz $LOCAL
cd $LOCAL

run_on_exit() {{
    set -v
    cp $LOCAL/* $PBS_O_WORKDIR
}}

trap run_on_exit EXIT

`which orca` {0}.in >& $PBS_O_WORKDIR/{0}.out
""".format(inpfile, ppn, time, queue, ptchrgfile, username = os.environ['USER'])

def template_pbsfile_coords_ptchrg(inpfile, ppn, time, queue, xyzfile, ptchrgfile):
    return """#!/bin/bash

#PBS -N {0}
#PBS -q {3}
#PBS -l nodes=1:ppn={1}
#PBS -l walltime={2}:00:00
#PBS -j oe
#PBS -l qos=low
#PBS -m abe
#PBS -M {username}@pitt.edu

module purge
module load orca/3.0.2

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
""".format(inpfile, ppn, time, queue, xyzfile, ptchrgfile, username = os.environ['USER'])

if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser()
    parser.add_argument('inpfilename',
                        help='the ORCA input file to submit')
    parser.add_argument('--xyzfile',
                        help='XYZ file containing molecular coordinates')
    parser.add_argument('--ptchrgfile',
                        help='XYZ file containing point charges (element as charge magnitude)')
    parser.add_argument('--ppn',
                        type=int,
                        default=4,
                        help='number of cores to run on (max shared=48, shared_large=16)')
    parser.add_argument('--time',
                        type=int,
                        default=96,
                        help='walltime to reserve (max 144 hours)')
    parser.add_argument('--queue',
                        default='shared',
                        help='queue to run in (typically shared or shared_large')
    args = parser.parse_args()
    inpfilename = os.path.splitext(args.inpfilename)[0]
    xyzfile = args.xyzfile
    ptchrgfile = args.ptchrgfile
    ppn = args.ppn
    time = args.time
    queue = args.queue

    if xyzfile is not None: xyzfile = os.path.splitext(xyzfile)[0]
    if ptchrgfile is not None: ptchrgfile = os.path.splitext(ptchrgfile)[0]

    pbsfilename = inpfilename + '.pbs'
    with open(pbsfilename, 'wb') as pbsfile:
        if xyzfile and ptchrgfile:
            pbsfile.write(template_pbsfile_coords_ptchrg(inpfilename, ppn, time, queue, xyzfile, ptchrgfile))
        elif xyzfile:
            pbsfile.write(template_pbsfile_coords(inpfilename, ppn, time, queue, xyzfile))
        elif ptchrgfile:
            pbsfile.write(template_pbsfile_ptchrg(inpfilename, ppn, time, queue, ptchrgfile))
        else:
            pbsfile.write(template_pbsfile(inpfilename, ppn, time, queue))

    print(pbsfilename)
