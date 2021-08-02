#!/usr/bin/env python

"""submit_molpro.py: A standalone script for submitting Molpro jobs to Haswell's
SLURM scheduler.

"""


def template_slurmfile_molpro(inpfile, ppn, time):
    """The template for a SLURM jobfile that calls Q-Chem."""
    return """#!/bin/bash

#SBATCH --job-name={inpfile}
#SBATCH --output={inpfile}.slurmout
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task={ppn}
#SBATCH --time=0-{time}:00:00
#SBATCH --partition=smp

module purge
module load molpro/2015.1.7

$(which molpro) -t ${{SLURM_CPUS_PER_TASK}} -d ${{SLURM_SCRATCH}} -o ${{SLURM_SUBMIT_DIR}}/{inpfile}.out {inpfile}.in
chmod 644 ${{SLURM_SUBMIT_DIR}}/{inpfile}.out
""".format(
        inpfile=inpfile, ppn=ppn, time=time, username=os.environ["USER"]
    )


if __name__ == "__main__":
    import argparse
    import os.path

    parser = argparse.ArgumentParser()
    parser.add_argument("inpfilename", help="the Molpro input file to submit", nargs="*")
    parser.add_argument("--ppn", type=int, default=12, help="number of cores to run on (max 12)")
    parser.add_argument("--time", type=int, default=24, help="walltime to reserve (max 72 hours)")
    args = parser.parse_args()

    for inpfilename in args.inpfilename:
        inpfilename = os.path.splitext(inpfilename)[0]

        slurmfilename = inpfilename + ".slurm"
        with open(slurmfilename, "w") as slurmfile:
            slurmfile.write(template_slurmfile_molpro(inpfilename, args.ppn, args.time))

        print(slurmfilename)
