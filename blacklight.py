#!/usr/bin/env python2

def grouper(n, iterable, fillvalue=None):
    """
    grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    """
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

def optimal_group_size(l, min_group_size=4, max_group_size=10):
    """
    Based on the size of the given list, determine the optimal group size
    or "packing" between the specified allowable range.
    """
    listlen = len(l)
    min_remainder, best_group_size = 999, 999
    counter = max_group_size
    while counter >= min_group_size:
        group_size = counter
        new_remainder = (group_size - (listlen % group_size))
        if new_remainder < min_remainder:
            min_remainder, best_group_size = new_remainder, group_size
        counter -= 1
    return best_group_size

def gen_job_strings(group):
    """
    Given a list of strings, generate the proper ORCA calls and determine the CPU
    offsets automatically.
    """
    proc_offset = 0
    orca_call = ""
    for f in group:
        orca_call += "dplace -c {0} `which orca` {1}.inp >& $PBS_O_WORKDIR/{1}.out &\n".format(proc_offset, f)
        proc_offset += 16
    return orca_call

def add_delimiters(l, delim):
    """
    Given a list of strings, join them all with a delimiter 
    (or any arbitrary string).
    """
    tmp = ""
    for element in l:
        if element == l[-1]:
            tmp += element
            return tmp
        tmp += element + delim

def gen_cp_string(l):
    """
    Generate the string for the copy command.
    """
    return "{" + add_delimiters(l, ",") + "}"


def gen_eprfile(charge, xyzfile, functional):
    """
    Generate an ORCA input file for performing an EPR calculation with the given charge, geometry, and functional.
    """
    return """! uks def2-tzvpp nori somf(1x) tightscf tightopt grid5

%pal
 nprocs 16
 end

* xyzfile {0} 2 {1}.xyz *

%scf
 guess pmodel
 end

%geom
 maxiter 512
 trust 0.3
 inhess almloef
 end

%method
 functional {2}
 end

%eprnmr
 tol 1e-10
 gtensor 1
 ori -3
 nuclei = all N  {{ aiso, adip, aorb, fgrad, rho }}
 nuclei = all Cu {{ aiso, adip, aorb, fgrad, rho }}
 printlevel 5
 end

""".format(charge, xyzfile, functional)

def gen_pbsfile(xyzfile, f):
    """
    Generate a Torque job submission file.
    """
    ncpus = len(f) * 16

    return """#!/bin/bash

#PBS -N {2}
#PBS -q batch
#PBS -l ncpus={1}
#PBS -l walltime=96:00:00
#PBS -j oe

source /usr/share/modules/init/bash
module load openmpi/1.6/intel
module use $HOME/modules
module load orca/3.0.0

workpath=$SCRATCH/orca-{2}-${{PBS_JOBID}}
mkdir $workpath
cp $PBS_O_WORKDIR/{3}.inp $workpath
cp $PBS_O_WORKDIR/{0}.xyz $workpath
cd $workpath

run_on_exit() {{
    set -v
    cp $workpath/* $PBS_O_WORKDIR
}}

trap run_on_exit EXIT

{4}
wait
""".format(xyzfile, ncpus, add_delimiters(f, "_"), gen_cp_string(f), gen_job_strings(f))

if __name__ == "__main__":
    import argparse
    import subprocess as sp
    from itertools import izip_longest

    parser = argparse.ArgumentParser(description="")
    parser.add_argument(dest="xname", metavar="<xyzfile>", type=str, help="")
    parser.add_argument("--charge", dest="charge", metavar="<charge>", type=int, default=0, help="")
    args = parser.parse_args()
    xname = args.xname
    charge = args.charge

    functionals = ["hfs", "xalpha", "lsd", "vwn5", "vwn3", "pwlda", "bnull", "bvwn", "bp", "pw91", "mpwpw", "mpwlyp",
               "blyp", "gp", "glyp", "pbe", "revpbe", "rpbe", "pwp", "olyp", "opbe", "xlyp", "b97-d", "b97-d3",
               "tpss", "b1lyp", "b3lyp", "b1p", "b3p", "g1lyp", "g3lyp", "g1p", "g3p", "pbe0", "pwp1", "mpw1pw",
               "mpw1lyp", "pw91_0", "o3lyp", "x3lyp", "pw6b95", "b97", "bhandhlyp", "tpssh", "tpss0", "b3lyp_tm",
               "b3lyp_g"]

    for group in grouper(optimal_group_size(functionals, 4, 8), functionals):
        funcs = [f for f in group if f is not None]
        for f in funcs:
            orcaname = f + ".inp"
            orcafile = open(orcaname, "w")
            print >> orcafile, gen_eprfile(charge, xname, f)
            orcafile.close()
        pbsname = add_delimiters(funcs, "_") + ".pbs"
        pbsfile = open(pbsname, "w")
        print >> pbsfile, gen_pbsfile(xname, funcs)
        pbsfile.close()
