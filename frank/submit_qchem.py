#!/usr/bin/env python

"""submit-qchem.py: A standalone script for submitting Q-Chem jobs to
Frank's PBS scheduler."""

from __future__ import print_function


def template_pbsfile_qchem(inpfile, ppn, time, queue, save, old, new, debug, release, lowqos):
    """The template for a PBS jobfile that calls Q-Chem."""
    saveflag = ''
    scratchdir = ''
    if save:
        saveflag = '-save '
        scratchdir = ' "{inpfile}.${{PBS_JOBID}}"'.format(inpfile=inpfile)
    module = 'qchem/4.3-trunk.20150505.omp.release'
    if old:
        module = 'qchem/4.2-trunk.20141216.omp.release'
    if new:
        module = 'qchem/4.3-trunk.20151005.omp.release'
    if debug:
        module = 'qchem/trunk_intel_debug'
    if release:
        module = 'qchem/trunk_intel_release'
    qosline = '#PBS -l qos=investor'
    if lowqos:
        qosline = '#PBS -l qos=low'
    return '''#!/usr/bin/env bash

#PBS -N {inpfile}
#PBS -q {queue}
#PBS -l nodes=1:ppn={ppn}
#PBS -l walltime={time}:00:00
{qosline}
#PBS -j oe
#PBS -m abe
#PBS -M {username}@pitt.edu

module purge
module load {module}

cp ${{PBS_O_WORKDIR}}/{inpfile}.in ${{LOCAL}}
cd ${{LOCAL}}

run_on_exit() {{
    set -v
    rm ${{LOCAL}}/pathtable
    cp -v -R ${{LOCAL}}/* ${{PBS_O_WORKDIR}}
}}

trap run_on_exit EXIT

$(which qchem) {saveflag}-nt {ppn} "{inpfile}.in" "${{PBS_O_WORKDIR}}/{inpfile}.out"{scratchdir}
'''.format(inpfile=inpfile,
           ppn=ppn,
           time=time,
           queue=queue,
           saveflag=saveflag,
           scratchdir=scratchdir,
           username=os.environ['USER'],
           module=module,
           qosline=qosline)


if __name__ == '__main__':
    import argparse
    import os.path

    parser = argparse.ArgumentParser()
    parser.add_argument('inpfilename',
                        help='the Q-Chem input file to submit')
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
                        help='queue to run in (typically shared or shared_large)')
    parser.add_argument('--save',
                        action='store_true',
                        help='save the scratch directory')
    parser.add_argument('--old',
                        action='store_true',
                        help='Use an older (known good) version of Q-Chem.')
    parser.add_argument('--new',
                        action='store_true',
                        help='Use a newer version of Q-Chem.')
    parser.add_argument('--debug',
                        action='store_true',
                        help='Use a debugging version of Q-Chem from trunk.')
    parser.add_argument('--release',
                        action='store_true',
                        help='Use a release version of Q-Chem from trunk.')
    parser.add_argument('--lowqos',
                        action='store_true',
                        help='set "#PBS -l qos=low"')
    args = parser.parse_args()
    inpfilename = os.path.splitext(args.inpfilename)[0]

    pbsfilename = inpfilename + '.pbs'
    with open(pbsfilename, 'w') as pbsfile:
        pbsfile.write(template_pbsfile_qchem(inpfilename,
                                             args.ppn,
                                             args.time,
                                             args.queue,
                                             args.save,
                                             args.old,
                                             args.new,
                                             args.debug,
                                             args.release,
                                             args.lowqos))

    print(pbsfilename)
