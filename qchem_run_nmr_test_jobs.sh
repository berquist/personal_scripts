#!/usr/bin/env bash

jobnames=(hcf3.den.dft.nmr hcf3.den.nmr hcf3.mo.nmr hcf3.nmr-dft nmr2 NMR nmrref)

cd $QC/test

for job in ${jobnames[*]}
do
    rm ${job}.out
    qchem ${job}.in ${job}.out
done
