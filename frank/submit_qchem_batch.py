#!/usr/bin/env python

from __future__ import print_function

import os.path


def template_pbsfile_batch(**jobvars):
    """The template for a PBS jobfile ..."""

    return """#!/usr/bin/env bash

#PBS -N {batchname}
#PBS -q {queue}
#PBS -l nodes={nodes}:ppn={ppn}
#PBS -l walltime={time}:00:00
#PBS -j oe
#PBS -m abe
#PBS -M {username}@pitt.edu

module purge
module load pbstools
module load openmpi/1.6.3-intel13
module load qchem/4.3-trunk.20150505.omp.release

cd ${{PBS_O_WORKDIR}}

mpiexec -np {nmpiprocs} --loadbalance --bind-to-core parallel-command-processor <<EOF
{jobstrings}
EOF
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
    parser.add_argument("--queue",
                        default="dist_small",
                        help="""The queue to run in.""")
    parser.add_argument("--walltime",
                        type=int,
                        default=144,
                        help="""The amount of time in hours to reserve (generally max 144).""")
    parser.add_argument("--ppn",
                        type=int,
                        default=16,
                        help="""The number of core per node to request.""")
    parser.add_argument("--batchname",
                        default="batch",
                        help="""The number of nodes to request.""")
    parser.add_argument("--nodes",
                        type=int,
                        default=1,
                        help="""The number of nodes to request.""")

    args = parser.parse_args()

    return args


def make_command_block_from_inputs(inputfiles):
    """Given a list of files names that are Q-Chem inputs, turn them into
    a formatted string block that can be used by
    parallel-command-processor.
    """
    qchem_command_template = "$(which qchem) -nt {ppj} {fnamestub}.in ${{PBS_O_WORKDIR}}/{fnamestub}.out".format
    job_commands = []
    for inputfile in inputfiles:
        stub = os.path.splitext(inputfile)[0]
        job_commands.append(qchem_command_template(ppj=args.ppj, fnamestub=stub))
    job_commands_section = "\n".join(job_commands)
    return job_commands_section


def main(args):
    """The top-level routine."""

    job_commands_section = make_command_block_from_inputs(args.inputfile)

    jobvars = dict()

    jobvars['queue'] = args.queue
    jobvars['nodes'] = args.nodes
    jobvars['ppn'] = args.ppn
    jobvars['time'] = args.walltime
    jobvars['nmpiprocs'] =  int((args.ppn * args.nodes) / args.ppj)
    jobvars['username'] = os.environ['USER']
    jobvars['jobstrings'] = job_commands_section
    jobvars['batchname'] = args.batchname

    with open("{0}.pbs".format(args.batchname), "w") as pbsfile:
        pbsfile.write(template_pbsfile_batch(**jobvars))

    return locals()


if __name__ == "__main__":

    args = getargs()
    main_locals = main(args)
