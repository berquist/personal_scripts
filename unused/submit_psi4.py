#!/usr/bin/env python

"""submit_psi4.py: A standalone script for submitting Psi4 jobs to
Haswell's SLURM scheduler.
"""


def template_slurmfile_psi4(inpfile, ppn, time, as_python):
    """The template for a SLURM jobfile that calls Psi4."""
    command = '$(which psi4) -n $SLURM_CPUS_PER_TASK "{inpfile}.in"'.format(inpfile=inpfile)
    if as_python:
        command = 'OMP_NUM_THREADS={ppn} $(which python) "{inpfile}.py"'.format(inpfile=inpfile)
    return """#!/usr/bin/env bash

#SBATCH --job-name={inpfile}
#SBATCH --output={inpfile}.slurmout
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task={ppn}
#SBATCH --time=0-{time}:00:00
#SBATCH --partition=smp

module purge
module load python/anaconda3

{command}
chmod 644 "$SLURM_SUBMIT_DIR/{inpfile}.out"
""".format(
        command=command, inpfile=inpfile, ppn=ppn, time=time
    )


if __name__ == "__main__":
    import argparse
    import os.path

    parser = argparse.ArgumentParser()
    parser.add_argument("inpfilename", help="the input file to submit", nargs="*")
    parser.add_argument("--ppn", type=int, default=12, help="number of cores to run on (max 12)")
    parser.add_argument("--time", type=int, default=24, help="walltime to reserve (max 144 hours)")
    parser.add_argument(
        "--as-python", action="store_true", help="Is the input file actually a Python script?"
    )
    args = parser.parse_args()

    for inpfilename in args.inpfilename:
        inpfilename = os.path.splitext(inpfilename)[0]

        slurmfilename = inpfilename + ".slurm"
        with open(slurmfilename, "w") as slurmfile:
            slurmfile.write(
                template_slurmfile_psi4(inpfilename, args.ppn, args.time, args.as_python)
            )
        print(slurmfilename)
