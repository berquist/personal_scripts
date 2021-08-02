#!/usr/bin/env python

"""submit_qchem.py: A standalone script for submitting Q-Chem jobs to
Haswell's SLURM scheduler.
"""


def template_slurmfile_qchem(inpfile, ppn, time, save, debug, release, sam):
    """The template for a SLURM jobfile that calls Q-Chem."""
    saveflag = ""
    scratchdir = ""
    if save:
        saveflag = "-save "
        scratchdir = ' "{inpfile}.$SLURM_JOB_ID"'.format(inpfile=inpfile)
    module = "qchem/trunk_intel_release"
    if debug:
        module = "qchem/trunk_intel_debug"
    if sam:
        module = "qchem/5.0"
    return """#!/bin/bash

#SBATCH --job-name={inpfile}
#SBATCH --output={inpfile}.slurmout
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task={ppn}
#SBATCH --time=0-{time}:00:00
#SBATCH --partition=smp
#SBATCH --mail-type=ALL
#SBATCH --mail-user={username}@pitt.edu

module purge
module load {module}

$(which qchem) {saveflag}-nt $SLURM_CPUS_PER_TASK "{inpfile}.in" "$SLURM_SUBMIT_DIR/{inpfile}.out"{scratchdir}
chmod 644 "$SLURM_SUBMIT_DIR/{inpfile}.out"
""".format(
        inpfile=inpfile,
        ppn=ppn,
        time=time,
        saveflag=saveflag,
        scratchdir=scratchdir,
        username=os.environ["USER"],
        module=module,
    )


if __name__ == "__main__":
    import argparse
    import os.path

    parser = argparse.ArgumentParser()
    parser.add_argument("inpfilename", help="the Q-Chem input file to submit", nargs="*")
    parser.add_argument("--ppn", type=int, default=1, help="number of cores to run on (max 24)")
    parser.add_argument("--time", type=int, default=1, help="walltime to reserve (max 72 hours)")
    parser.add_argument("--save", action="store_true", help="save the scratch directory")
    parser.add_argument(
        "--debug", action="store_true", help="Use a debugging version of Q-Chem from trunk."
    )
    parser.add_argument(
        "--release", action="store_true", help="Use a release version of Q-Chem from trunk."
    )
    parser.add_argument(
        "--sam", action="store_true", help="Use the cluster (customer) copy of Q-Chem."
    )
    args = parser.parse_args()

    for inpfilename in args.inpfilename:
        inpfilename = os.path.splitext(inpfilename)[0]

        slurmfilename = inpfilename + ".slurm"
        with open(slurmfilename, "w") as slurmfile:
            slurmfile.write(
                template_slurmfile_qchem(
                    inpfilename, args.ppn, args.time, args.save, args.debug, args.release, args.sam
                )
            )

        print(slurmfilename)
