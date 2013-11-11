#!/bin/bash

#PBS -j oe
#PBS -q ishared
#PBS -l walltime=48:00:00
#PBS -l nodes=1:ppn=16

JOB=pt17_ni1
IN=$JOB.in
OUT=$JOB.out

module purge
module load espresso/5.0-intel12-openmpi

cd $PBS_O_WORKDIR

sed -i "s%pseudo_dir *=.*%pseudo_dir = '$ESPRESSO_PSEUDO'%" $IN
sed -i "s%outdir *=.*%outdir = '$LOCAL'%" $IN

cp $IN $LOCAL
cd $LOCAL

trap "cp -r $LOCAL/* $PBS_O_WORKDIR/" EXIT

prun pw.x < $IN > $PBS_O_WORKDIR/$OUT