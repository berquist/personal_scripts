#!/usr/bin/env python2

def template_pbsfile(inpfile, ppn, time, queue, save, old):
    save = ''
    scratchdir = ''
    if save:
        save = '-save '
        scratchdir = ' {inpfile}.${{PBS_JOBID}}'.format(inpfile=inpfile)
    module = 'qchem/dlambrecht/4.2-trunk.20140824.omp.release'
    if old:
        module = 'qchem/dlambrecht/4.1-trunk.20130919.omp.ccman2'
    return '''#!/bin/bash

#PBS -N {inpfile}
#PBS -q {queue}
#PBS -l nodes=1:ppn={ppn}
#PBS -l walltime={time}:00:00
#PBS -j oe
#PBS -l qos=low
#PBS -m abe
#PBS -M {username}@pitt.edu

module purge
module load intel/2013.0
module load {module}

cp $PBS_O_WORKDIR/{inpfile}.in $LOCAL
cd $LOCAL

run_on_exit() {{
    set -v
    rm $LOCAL/pathtable
    cp -v -R $LOCAL/* $PBS_O_WORKDIR
}}

trap run_on_exit EXIT

`which qchem` {save}-nt {ppn} {inpfile}.in $PBS_O_WORKDIR/{inpfile}.out{scratchdir}
'''.format(inpfile=inpfile,
           ppn=ppn,
           time=time,
           queue=queue,
           save=save,
           scratchdir=scratchdir,
           username=os.environ['USER'],
           module=module)


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
    args = parser.parse_args()
    inpfilename = os.path.splitext(args.inpfilename)[0]
    ppn = args.ppn
    time = args.time
    queue = args.queue
    save = args.save
    old = args.old

    pbsfilename = inpfilename + '.pbs'
    with open(pbsfilename, 'wb') as pbsfile:
        pbsfile.write(template_pbsfile(inpfilename, ppn, time, queue, save, old))

    print(pbsfilename)
