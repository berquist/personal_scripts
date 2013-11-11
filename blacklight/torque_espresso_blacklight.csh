#!/bin/csh

#PBS -j oe
#PBS -q batch
#PBS -l walltime=96:00:00
#PBS -l ncpus=16

JOB=pt17_ni1
IN=$JOB.in
OUT=$JOB.out

module purge
module load espresso/5.0.2

cd $PBS_O_WORKDIR

sed -i "s%pseudo_dir *=.*%pseudo_dir = '$ESPRESSO_PSEUDO'%" $IN
sed -i "s%outdir *=.*%outdir = '$LOCAL'%" $IN

mkdir $SCRATCH/espresso_${PBS_JOBID}
cp $IN $$SCRATCH/espresso_${PBS_JOBID}
cd $SCRATCH/espresso_${PBS_JOBID}

trap "cp -r $SCRATCH/espresso_${PBS_JOBID}/* $PBS_O_WORKDIR/" EXIT

prun pw.x < $IN > $PBS_O_WORKDIR/$OUT
