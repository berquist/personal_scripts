# Sample PBS job script
#
# Copy this script, customize it and then submit it with the ``qsub''
# command. For example:
#
# cp pbs-template.sh myjob-pbs.sh
# {emacs|vi} myjob-pbs.sh
# qsub myjob-pbs.sh
#
# PBS directives are fully documented in the ``qsub'' man page. Directives
# may be specified on the ``qsub'' command line, or embedded in the
# job script.
#
# For example, if you want the batch job to inherit all your environment
# variables, use the ``V'' switch when you submit the job script:
#
# qsub -V myjob-pbs.sh
#
# or uncomment the following line by removing the initial ``###''
### #PBS -V

# Note: group all PBS directives at the beginning of your script.
# Any directives placed after the first shell command will be ignored.

### Set the job name
#PBS -N myjob

### Run in the queue named "batch"
#PBS -q batch

### Use the bourne shell
#PBS -S /bin/sh

### Remove only the three initial "#" characters before #PBS
### in the following lines to enable:
###
### To send email when the job is completed:
### #PBS -m ae
### #PBS -M your@email.address

### Optionally set the destination for your program's output
### Specify localhost and an NFS filesystem to prevent file copy errors.
### #PBS -e localhost:$HOME/myjob.err
### #PBS -o localhost:$HOME/myjob.log

### Specify the number of cpus for your job.  This example will allocate 4 cores
### using 2 processors on each of 2 nodes.
### #PBS -l nodes=2:ppn=2

### Tell PBS how much memory you expect to use. Use units of 'b','kb', 'mb' or 'gb'.
### #PBS -l mem=256m

### Tell PBS the anticipated run-time for your job, where walltime=HH:MM:SS
### #PBS -l walltime=1:00:00

### Switch to the working directory; by default TORQUE launches processes
### from your home directory.
cd $PBS_O_WORKDIR
echo Working directory is $PBS_O_WORKDIR

# Calculate the number of processors allocated to this run.
NPROCS=`wc -l < $PBS_NODEFILE`

# Calculate the number of nodes allocated.
NNODES=`uniq $PBS_NODEFILE | wc -l`

### Display the job context
echo Running on host `hostname`
echo Time is `date`
echo Directory is `pwd`
echo Using ${NPROCS} processors across ${NNODES} nodes

### OpenMPI will automatically launch processes on all allocated nodes.
## MPIRUN=`which mpirun`
## ${MPIRUN} my-openmpi-program

### Or, just run your serial program
## $HOME/my-program


# PBS environment variables available in every batch job:
#
# $PBS_ENVIRONMENT set to PBS_BATCH to indicate that the job is a batch job; otherwise,
#                  set to PBS_INTERACTIVE to indicate that the job is a PBS interactive job
# $PBS_JOBID       the job identifier assigned to the job by the batch system
# $PBS_JOBNAME     the job name supplied by the user
# $PBS_NODEFILE    the name of the file that contains the list of nodes assigned to the job
# $PBS_QUEUE       the name of the queue from which the job is executed
# $PBS_O_HOME      value of the HOME variable in the environment in which qsub was executed
# $PBS_O_LANG      value of the LANG variable in the environment in which qsub was executed
# $PBS_O_LOGNAME   value of the LOGNAME variable in the environment in which qsub was executed
# $PBS_O_PATH      value of the PATH variable in the environment in which qsub was executed
# $PBS_O_MAIL      value of the MAIL variable in the environment in which qsub was executed
# $PBS_O_SHELL     value of the SHELL variable in the environment in which qsub was executed
# $PBS_O_TZ        value of the TZ variable in the environment in which qsub was executed
# $PBS_O_HOST      the name of the host upon which the qsub command is running
# $PBS_O_QUEUE     the name of the original queue to which the job was submitted
# $PBS_O_WORKDIR   the absolute path of the current working directory of the qsub command
#
# End of example PBS script
