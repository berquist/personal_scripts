#!/usr/bin/env bash

# extract_CO2.sh: Extract the CO2 from a "cluster" XYZ file and form a
# new Q-Chem input file using it in place of the cluster.

xyzfiles=$(ls CO2_BMIM*freq*.xyz)

for xyzfile in ${xyzfiles[@]}; do

    # prepare the extracted coordinates
    prefix=$(echo "${xyzfile}" | cut -d "." -f 1)
    remainder=$(echo "${xyzfile}" | cut -d "." -f 2-)
    clustername=$(echo "${prefix}" | cut -d "_" -f 2-)
    newprefix="CO2_from_cluster_${clustername}"
    newxyzfile="${newprefix}.${remainder}"
    extracted_coordinates=$(cat "${xyzfile}" | tail -n 4 | head -n 3)
    echo "${newxyzfile}"
    echo -e "3\n\n${extracted_coordinates}" > "${newxyzfile}"

    # prepare the input files for these extracted coordinates
    inputfile="${xyzfile//.xyz/.in}"
    newinputfile="${newxyzfile//.xyz/.in}"
    rem=$(sed '/\$molecule/,/\$end/d' < "${inputfile}")
    molecule="\$molecule\n0 1\n${extracted_coordinates}\n\$end"
    echo "${newinputfile}"
    echo -e "${rem}\n\n${molecule}" > "${newinputfile}"
done
