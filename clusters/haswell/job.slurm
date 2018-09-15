#!/usr/bin/env bash
#SBATCH --job-name=test
#SBATCH --output=test.out
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=12
#SBATCH --time=0-00:30:00
#SBATCH --partition=smp-high

# Load the module
module purge

# Build the machines file
srun -N $SLURM_NNODES -n 1 hostname > $SLURM_SUBMIT_DIR/machinefile

# Load the environment
source /ihome/crc/build/qchem/4.3/qcenv.sh

# Some QChem specific environment variables
export QCSCRATCH=$SLURM_SUBMIT_DIR
export QCLOCALSCR=$SLURM_SCRATCH
export QCMACHINEFILE=$SLURM_SUBMIT_DIR/machinefile

# Run the hybrid MPI/OpenMP style QChem job
qchem -np $SLURM_NNODES -nt $SLURM_NTASKS_PER_NODE co2_optfreq.qc co2_optfreq.out
