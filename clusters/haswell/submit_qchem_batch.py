#!/usr/bin/env python


import os.path


def template_slurmfile_batch(**jobvars):
    """The template for a SLURM jobfile ..."""

    jobvars['module'] = 'qchem/trunk_intel_release'

    cluster = jobvars['cluster']
    partition = jobvars['partition']

    return """#!/bin/bash

#SBATCH --job-name={batchname}
#SBATCH --output={batchname}.slurmout
#SBATCH --cluster={cluster}
#SBATCH --partition={partition}
#SBATCH --nodes={nnodes}
#SBATCH --ntasks={ntasks}
#SBATCH --time=0-{time}:00:00

module purge
module load {module}

nodelist=($(scontrol show hostname $SLURM_NODELIST))

ulimit -s unlimited
export LC_COLLATE=C

{jobstrings}
wait
""".format(**jobvars)


def getargs():
    """Parse command-line arguments."""

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("inputfile",
                        nargs="+",
                        help="""One or more Q-Chem calculation input files to run in the batch job.""")
    parser.add_argument("--ppj",
                        type=int,
                        default=1,
                        help="""The number of cores to use per individual calculation.""")
    parser.add_argument("--cluster",
                        default="smp",
                        help="""TODO""")
    parser.add_argument("--partition",
                        default="smp",
                        help="""TODO""")
    parser.add_argument("--walltime",
                        type=int,
                        default=144,
                        help="""The amount of time in hours to reserve (generally max 144).""")
    parser.add_argument("--ppn",
                        type=int,
                        default=28,
                        help="""The number of core per node to request.""")
    parser.add_argument("--batchname",
                        default="batch",
                        help="""TODO""")
    parser.add_argument("--nnodes",
                        type=int,
                        default=1,
                        help="""The number of nodes to request.""")

    args = parser.parse_args()

    return args


def make_command_block_from_inputs(inputfiles, nnodes, ppj):
    """Given a list of files names that are Q-Chem inputs, turn them into
    a formatted string block that can be used by
    parallel-command-processor.
    """
    qchem_command_template = 'srun --nodes=1 --ntasks=1 --cpus-per-task={ppj} --exclusive -w ${{nodelist[{nodeidx}]}} $(which qchem) -nt {ppj} {fnamestub}.in "${{SLURM_SUBMIT_DIR}}"/{fnamestub}.out &'.format
    job_commands = []
    for i, inputfile in enumerate(inputfiles):
        stub = os.path.splitext(inputfile)[0]
        # round robin
        nodeidx = i % nnodes
        job_commands.append(qchem_command_template(nodeidx=nodeidx, fnamestub=stub, ppj=ppj))
    job_commands_section = "\n".join(job_commands)
    return job_commands_section


def main(args):
    """The top-level routine."""

    jobvars = dict()

    if args.cluster == 'smp':
        assert args.partition in ('smp', 'high-mem')
        if args.partition == 'smp':
            ppn = 24
        elif args.partition == 'high-mem':
            ppn = 12
        assert args.ppn <= ppn
        assert args.ppj <= ppn
        assert args.nnodes == 1
    elif args.cluster == 'mpi':
        assert args.partition in ('opa',)
        ppn = 28
        assert args.ppn <= ppn
        assert args.ppj <= ppn
        assert args.nnodes >= 2
    else:
        pass

    job_commands_section = make_command_block_from_inputs(args.inputfile, args.nnodes, args.ppj)

    jobvars['cluster'] = args.cluster
    jobvars['partition'] = args.partition
    jobvars['nnodes'] = args.nnodes
    jobvars['ppn'] = args.ppn
    jobvars['ppj'] = args.ppj
    jobvars['time'] = args.walltime
    # jobvars['ntasks'] = int((args.ppn * args.nnodes) / args.ppj)
    # *Maximum* number of tasks. Total is actually above. As long as
    # *cpus-per-task is set, this can't be oversubscribed.
    jobvars['ntasks'] = int(args.ppn * args.nnodes)
    jobvars['username'] = os.environ['USER']
    jobvars['jobstrings'] = job_commands_section
    jobvars['batchname'] = args.batchname

    with open("{0}.slurm".format(args.batchname), "w") as slurmfile:
        slurmfile.write(template_slurmfile_batch(**jobvars))

    return locals()


if __name__ == "__main__":

    args = getargs()
    main_locals = main(args)
