#!/usr/bin/env bash
#SBATCH --cluster=mpi
#SBATCH --nodes=2
#SBATCH --ntasks=56
#SBATCH --time=1:00:00
#SBATCH --job-name=many-serial-jobs
#SBATCH --output=many-serial-jobs.out

# Conguration
CPUS_PER_TASK=7

# Useful BASH arrays
jobs=({1..8}.g09)
nodes=($(scontrol show hostname $SLURM_NODELIST))

# We want to run in the $SLURM_SCRATCH dir
cd $SLURM_SCRATCH

# Copy inputs to the scratch space, for every node!
for i in ${jobs[@]}; do
    sbcast $SLURM_SUBMIT_DIR/$i $SLURM_SCRATCH/$i
done

# Set a trap to copy the outputs back
run_on_exit(){
    for job in ${jobs[@]}; do
        jobname=$(basename -s .g09 $job)
        cp $jobname.{out,chk} $SLURM_SUBMIT_DIR
    done
}
trap run_on_exit EXIT

# The gaussian module
module purge
module load gaussian/D.01

# Silly quantum chemistry programs
ulimit -s unlimited
export LC_COLLATE=C

# Round robin submit
for ((n = 0; n < ${#jobs[@]}; n++)); do
    index=$(expr $n % ${#nodes[@]})
    jobname=$(basename -s .g09 ${jobs[$n]})
    srun --nodes=1 --ntasks=1 --cpus-per-task=$CPUS_PER_TASK --exclusive -w ${nodes[$index]} g09 < $jobname.g09 > $SLURM_SUBMIT_DIR/$jobname.out &
done
wait

run_on_exit
