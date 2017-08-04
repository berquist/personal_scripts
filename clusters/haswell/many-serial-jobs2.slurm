#!/usr/bin/env bash
#SBATCH --cluster=smp
#SBATCH --partition=smp
#SBATCH --nodes=1
#SBATCH --ntasks=12
#SBATCH --cpus-per-task=2
#SBATCH --time=1:00:00
#SBATCH --job-name=many-serial-jobs
#SBATCH --output=many-serial-jobs.slurmout

jobs=(md10_{1..24}.in)
nodes=($(scontrol show hostname $SLURM_NODELIST))

module purge
module load qchem/trunk_intel_release

ulimit -s unlimited
export LC_COLLATE=C

# Round robin submit
for ((n = 0; n < ${#jobs[@]}; n++)); do
    index=$(expr $n % ${#nodes[@]})
    jobname=$(basename -s .in ${jobs[$n]})
    srun --ntasks=1 --exclusive -w ${nodes[$index]} $(which qchem) -nt $SLURM_CPUS_PER_TASK ${jobname}.in $SLURM_SUBMIT_DIR/${jobname}.out &
done
wait
