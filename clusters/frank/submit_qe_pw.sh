#!/bin/bash

# This script submits Quantum Espresso jobs.
# It also properly modifies the user's output location in the
#   QE input file.

if [ "$#" -ne 3 ]; then
    echo "Usage: submit_qe_pw <input file> <ppn> <walltime (in hrs)>"
    exit 1
fi

JOBNAME=${1/.in/}
PPN=$2
TIME=$3

IN=${JOBNAME}.in
OUT=${JOBNAME}.out

cat <<EOF > $PWD/run_qe_pw.${JOBNAME}.pbs
#!/bin/bash

#PBS -N ${JOBNAME}
#PBS -q ishared
#PBS -l nodes=1:ppn=${PPN}
#PBS -l walltime=${TIME}:00:00
#PBS -j oe
#PBS -l qos=low
#PBS -m abe
#PBS -M ${USER}@pitt.edu

JOB=${JOBNAME}
IN=\$JOB.in
OUT=\$JOB.out

module rm openmpi fftw espresso
module load espresso/5.0-intel12-openmpi

# Don't forget to set outdir and pseudo_dir
# to appropriate values in your input file.
# For example, you can put provide dummy arguments
# to psuedo_dir and outdir in the input file and
# adjust them at run time.
# sed -i "s%pseudo_dir *=.*%pseudo_dir='\$ESPRESSO_PSEUDO'%" input.file
# sed -i "s%outdir *=.*%outdir='\$LOCAL'%" input.file

cd \$PBS_O_WORKDIR

sed -i "s%pseudo_dir *=.*%pseudo_dir = '\$ESPRESSO_PSEUDO'%I" \$IN
sed -i "s%outdir *=.*%outdir = '\$LOCAL'%I" \$IN

cp \$IN \$LOCAL
cd \$LOCAL
trap "cp -r \$LOCAL \$PBS_O_WORKDIR/" EXIT
`3
prun pw.x < \$IN > \$PBS_O_WORKDIR/\$OUT

EOF

qsub $PWD/run_qe_pw.${JOBNAME}.pbs
