#!/usr/bin/env python

"""submit_dalton.py: A standalone script for submitting DALTON jobs to
Haswell's SLURM scheduler.
"""

from __future__ import print_function


def template_slurmfile_dalton(inpfile, ppn, time, extrafiles):
    """The template for a SLURM jobfile that calls DALTON."""

    copy_string_template = 'cp "$SLURM_SUBMIT_DIR"/{} "$LOCAL"\n'
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
    module = 'dalton/2016.2-i2017.1-mkl_parallel-omp'
    return '''#!/bin/bash

#SBATCH --job-name={inpfile}
#SBATCH --output={inpfile}.slurmout
#SBATCH --nodes=1
#SBATCH --ntasks-per-node={ppn}
#SBATCH --time=0-{time}:00:00

module purge
module load intel/2017.1.132
module load mkl/2017.1.132
module load {module}

mkdir -p "$LOCAL"

cp "$SLURM_SUBMIT_DIR"/{inpfile}.dal "$LOCAL"
{extrafiles}cd "$LOCAL"

run_on_exit() {{
    set -v
    find "$LOCAL" -type f -exec chmod 644 '{{}}' \;
    cp -v -R "$LOCAL"/DALTON_scratch_{username}/* "$SLURM_SUBMIT_DIR"
}}

trap run_on_exit EXIT

$(which dalton) -omp {ppn} -noarch -nobackup -d -ow -w "$SLURM_SUBMIT_DIR" {inpfile}.dal
chmod 644 "$SLURM_SUBMIT_DIR"/{inpfile}.out
'''.format(inpfile=inpfile,
           ppn=ppn,
           time=time,
           module=module,
           username=os.environ['USER'],
           extrafiles=joined_extrafiles)


if __name__ == "__main__":
    import argparse
    import os.path

    parser = argparse.ArgumentParser()
    parser.add_argument('inpfilename',
                        help='the DALTON input file to submit',
                        nargs='*')
    parser.add_argument('--ppn',
                        type=int,
                        default=12,
                        help='number of cores to run on (max 12)')
    parser.add_argument('--time',
                        type=int,
                        default=24,
                        help='walltime to reserve (max 144 hours)')
    parser.add_argument('--extrafiles',
                        help='An arbitrary number of files to copy to $LOCAL.',
                        nargs='*')
    args = parser.parse_args()

    for inpfilename in args.inpfilename:
        inpfilename = os.path.splitext(inpfilename)[0]

        slurmfilename = inpfilename + '.slurm'
        with open(slurmfilename, 'w') as slurmfile:
            slurmfile.write(template_slurmfile_dalton(inpfilename,
                                                      args.ppn,
                                                      args.time,
                                                      args.extrafiles))

        print(slurmfilename)
