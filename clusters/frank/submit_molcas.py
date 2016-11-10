#!/usr/bin/env python

"""submit-molcas.py: A standalone script for submitting Molcas jobs to
Frank's PBS scheduler.
"""

from __future__ import print_function


def template_pbsfile_molcas(inpfile, ppn, time, queue, extrafiles, save):
    """The template for a PBS jobfile that calls Molcas."""
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
    savemap = {False: 'no', True: 'yes'}
    return """#!/usr/bin/env bash

#PBS -N {inpfile}
#PBS -q {queue}
#PBS -l nodes=1:ppn={ppn}
#PBS -l walltime={time}:00:00
#PBS -j oe
#PBS -m abe
#PBS -M {username}@pitt.edu

module purge
module load molcas/8.0

export CPUS=`wc -l $PBS_NODEFILE | cut -d" " -f1`
export MOLCAS_KEEP_WORKDIR={keep_workdir}

cp $PBS_O_WORKDIR/{inpfile}.in $LOCAL
{extrafiles}cd $LOCAL

run_on_exit() {{
    set -v
    find ${{LOCAL}} -type f -exec chmod 644 '{{}}' \;
    cp -R ${{LOCAL}}/* ${{PBS_O_WORKDIR}}
}}

trap run_on_exit EXIT

$(which molcas) {inpfile}.in >& ${{PBS_O_WORKDIR}}/{inpfile}.out
chmod 644 ${{PBS_O_WORKDIR}}/{inpfile}.out
""".format(inpfile=inpfile,
           ppn=ppn,
           time=time,
           queue=queue,
           username=os.environ['USER'],
           extrafiles=joined_extrafiles,
           keep_workdir=savemap[save])


if __name__ == "__main__":
    import argparse
    import os.path

    parser = argparse.ArgumentParser()
    parser.add_argument('inpfilename',
                        help='the Molcas input file to submit')
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
    parser.add_argument('--save',
                        action='store_true',
                        help='save the scratch directory')
    args = parser.parse_args()
    inpfilename = os.path.splitext(args.inpfilename)[0]

    pbsfilename = inpfilename + '.pbs'
    with open(pbsfilename, 'w') as pbsfile:
        pbsfile.write(template_pbsfile_molcas(inpfilename,
                                              args.ppn,
                                              args.time,
                                              args.queue,
                                              args.extrafiles,
                                              args.save))

    print(pbsfilename)
