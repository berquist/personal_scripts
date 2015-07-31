#!/usr/bin/env python

"""submit-aces.py: A standalone script for submitting ACES jobs to
Frank's PBS scheduler.
"""

from __future__ import print_function


def template_pbsfile_aces(inpfile, ppn, time, queue, extrafiles):
    """The template for a PBS jobfile that calls ACES."""
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
    return """#!/usr/bin/env bash

#PBS -N {inpfile}
#PBS -q {queue}
#PBS -l nodes=1:ppn={ppn}
#PBS -l walltime={time}:00:00
#PBS -j oe
#PBS -m abe
#PBS -M {username}@pitt.edu

module purge
module load aces/3.0.7-i2013.0-ompi1.6.3

cp $ACES_ROOT/tests/GENBAS $LOCAL
cp $PBS_O_WORKDIR/ZMAT $LOCAL
{extrafiles}cd $LOCAL

run_on_exit() {{
    set -v
    cp -R $LOCAL/* $PBS_O_WORKDIR
}}

trap run_on_exit EXIT

$(which mpirun) -np {ppn} $(which xaces3) >& $PBS_O_WORKDIR/{inpfile}.out
""".format(inpfile=inpfile,
           ppn=ppn,
           time=time,
           queue=queue,
           username=os.environ['USER'],
           extrafiles=joined_extrafiles)


if __name__ == "__main__":
    import argparse
    import os.path

    parser = argparse.ArgumentParser()
    parser.add_argument('inpfilename',
                        help='the name of the job/ACES output file')
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
    parser.add_argument('--extrafiles',
                        help='An arbitrary number of files to copy to $LOCAL.',
                        nargs='*')
    args = parser.parse_args()
    inpfilename = os.path.splitext(args.inpfilename)[0]

    pbsfilename = inpfilename + '.pbs'
    with open(pbsfilename, 'w') as pbsfile:
        pbsfile.write(template_pbsfile_aces(inpfilename,
                                            args.ppn,
                                            args.time,
                                            args.queue,
                                            args.extrafiles))

    print(pbsfilename)
