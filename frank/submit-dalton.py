#!/usr/bin/env python

"""submit-dalton.py: A standalone script for submitting DALTON jobs to
Frank's PBS scheduler.
"""

from __future__ import print_function

# import logging
import sys

# logging.basicConfig(level=logging.INFO)


def determine_parallelism(args):
    """Based on the command line arguments, determine whether or not to
    use MPI or OpenMP parallelism.

    Edge cases
    ==========
    1. Both flags present: MPI
    2. No flags present: OpenMP
    """

    if args.omp and args.mpi:
        return 'mpi'
    elif args.omp and not args.mpi:
        return 'omp'
    elif not args.omp and args.mpi:
        return 'mpi'
    elif not args.omp and not args.mpi:
        return 'omp'
    else:
        logging.error("Bad arguments to parallel flags")
        sys.exit(1)


def template_pbsfile_dalton(inpfile, ppn, time, queue, parimpl, extrafiles):
    """The template for a PBS jobfile that calls DALTON."""

    copy_string_template = "cp $PBS_O_WORKDIR/{} $LOCAL\n"
    if extrafiles is None:
        joined_extrafiles = ""
    elif isinstance(extrafiles, list):
        copy_strings = []
        for extrafile in extrafiles:
            copy_string = copy_string_template.format(extrafile)
            copy_strings.append(copy_string)
        joined_extrafiles = "".join(copy_strings)
    else:
        joined_extrafiles = copy_string_template.format(extrafiles)
    # Are we using an OpenMPI- or OpenMP-parallel version?
    if parimpl == 'mpi':
        parflag = '-N'
        module = 'dalton/2015-i2013.0-mkl-mpi'
    elif parimpl == 'omp':
        parflag = '-nt'
        module = 'dalton/2015-i2013.0-mkl-omp'
    else:
        raise
    return """#!/usr/bin/env bash

#PBS -N {inpfile}
#PBS -q {queue}
#PBS -l nodes=1:ppn={ppn}
#PBS -l walltime={time}:00:00
#PBS -j oe
#PBS -m abe
#PBS -M {username}@pitt.edu

module purge
module load {module}

cp $PBS_O_WORKDIR/{inpfile}.dal $LOCAL
{extrafiles}cd $LOCAL

run_on_exit() {{
    set -v
    cp -R $LOCAL/* $PBS_O_WORKDIR
}}

trap run_on_exit EXIT

`which dalton` {parflag} {ppn} {inpfile}.dal
""".format(inpfile=inpfile,
           ppn=ppn,
           time=time,
           queue=queue,
           parflag=parflag,
           module=module,
           username=os.environ['USER'],
           extrafiles=joined_extrafiles)


if __name__ == "__main__":
    import argparse
    import os.path

    parser = argparse.ArgumentParser()
    parser.add_argument('inpfilename',
                        help='the DALTON input file to submit')
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
    parser.add_argument('--omp',
                        help='Use the OpenMP-parallel version.',
                        action='store_true')
    parser.add_argument('--mpi',
                        help='Use the MPI-parallel version (OpenMPI).',
                        action='store_true')
    parser.add_argument('--extrafiles',
                        help='An arbitrary number of files to copy to $LOCAL.',
                        nargs='*')
    args = parser.parse_args()
    parimpl = determine_parallelism(args)
    inpfilename = os.path.splitext(args.inpfilename)[0]

    pbsfilename = inpfilename + '.pbs'
    with open(pbsfilename, 'w') as pbsfile:
        pbsfile.write(template_pbsfile_dalton(inpfilename,
                                              args.ppn,
                                              args.time,
                                              args.queue,
                                              parimpl,
                                              args.extrafiles))

    # logging.info(pbsfilename)
    print(pbsfilename)
