#!/usr/bin/env bash

#SBATCH --cluster=mpi
#SBATCH --nodes=2
#SBATCH --ntasks=56
#SBATCH --time=1:00:00
#SBATCH --job-name=many-serial-jobs
#SBATCH --output=many-serial-jobs.slurmout

CPUS_PER_TASK=7

jobs=({1..8}.g09)
nodes=($(scontrol show hostname $SLURM_NODELIST))

cd $SLURM_SCRATCH

ulimit -s unlimited
export LC_COLLATE=C

# Round robin submit
for ((n = 0; n < ${#jobs[@]}; n++)); do
    index=$(expr $n % ${#nodes[@]})
    jobname=$(basename -s .g09 ${jobs[$n]})
    string="srun --nodes=1 --ntasks=1 --cpus-per-task=$CPUS_PER_TASK --exclusive -w ${nodes[$index]} g09 < $jobname.g09 > $SLURM_SUBMIT_DIR/$jobname.out &"
    echo "${string}"
done
wait
