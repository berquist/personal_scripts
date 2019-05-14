#!/usr/bin/env bash

set -euo pipefail

# run_firefly.bash: Given an input file with a name like `my_firefly_job.inp`,
# make a directory called `my_firefly_job`, copy the input into
# `my_firefly_job/INPUT`, run the Firefly calculation, move the output back
# into the original directory, and delete the `my_firefly_job` directory.

fullpath=$(realpath ${1})
inputfilename=${fullpath##*/}
stub=${inputfilename%.*}

firefly=$(realpath $(command -v firefly))
fireflydir=$(dirname ${firefly})
echo $fireflydir

if [[ -d ${stub} ]]; then
    rm -rf ${stub}
fi
mkdir ${stub} || exit 1
cp -a ${fullpath} ${stub}/INPUT
(
    cd ${stub}
    # for extension in dftd.ex fastdiag.ex ffp2p.ex p4stuff.ex pcgp2p.ex; do
    #     cp -a ${fireflydir}/${extension} .
    # done
    $(command -v firefly) -nompi -o OUTPUT
)
cp -a ${stub}/OUTPUT ${stub}.out
rm -rf ${stub}

# From http://classic.chem.msu.su/gran/gamess/introlinux.html:

#   You should have a file named "input" in the current directory containing
#   the input information for the Firefly. By default, Firefly will write the
#   output to the stdout device, hence you should use an I/O redirection to
#   save it as a file. For example, you can use something like:

#   ./firefly8 >test.out 2>&1

#   or

#   ./firefly8 -o test.out

#   All the temporary files will be created in the current directory, so if
#   you want to run several Firefly jobs simultaneously, you should run them
#   in different directories. Insofar as the PUNCH file is always created with
#   the 'NEW' status, there should not be any previous PUNCH file in the
#   Firefly working directory. In general, it is recommended to delete all the
#   other temporary Firefly files (such as DICTNRY, etc...), before starting
#   next Firefly job, unless you want to use some restart options.

#   Probably, you will write some script to delete these files, create input,
#   and run Firefly with I/O redirection.
