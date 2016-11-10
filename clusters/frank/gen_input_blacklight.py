#!/usr/bin/env python

def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

def eprfile(charge, xyzfile, functional):
    """
    """
    return """! uks def2-tzvpp def2-tzvpp/j ri rijcosx somf(1x) tightscf tightopt grid5

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

def gen_job_string(f):
        proc_offset = 0
        orca_call = ""
        for job in f:
            orca_call += "dplace -c {0} `which orca` {1}.inp >& $PBS_O_WORKDIR/{1}.out &\n".format(proc_offset, job)
            proc_offset += 16
        return orca_call

def pbsfile(xyzfile, f):
    """
    """
    ncpus = len(f) * 16

    return """#!/bin/bash

#PBS -N
#PBS -q batch
#PBS -l ncpus={1}
#PBS -l walltime=96:00:00
#PBS -j oe

module load openmpi/1.6/intel
module use $HOME/modules
module load orca/3.0.0

set workpath $SCRATCH/orca-${{PBS_JOBID}}-{1}
mkdir $workpath
cp $PBS_O_WORKDIR/{1}.inp $workpath
cp $PBS_O_WORKDIR/{0}.xyz $workpath
cd $workpath

run_on_exit() {{
    set -v
    cp $workpath/* $PBS_O_WORKDIR
}}

trap run_on_exit EXIT

{}
wait
""".format(xyzfile, f1, f2, f3, f4)

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

    functionals = ["hfs", "xalpha", "lsd", "vwn5", "vwn3", "pwlda",
                   "bnull", "bvwn", "bp", "pw91", "mpwpw", "mpwlyp", "blyp", "gp", "glyp", "pbe", "revpbe", "rpbe", "pwp", "olyp", "opbe", "xlyp", "b97-d", "b97-d3",
                   "tpss",
                   "b1lyp", "b3lyp", "b1p", "b3p", "g1lyp", "g3lyp", "g1p", "g3p", "pbe0", "pwp1", "mpw1pw", "mpw1lyp", "pw91_1", "o3lyp", "x3lyp", "pw6b95", "b97", "bhandhlyp",
                   "tpssh", "tpssh0",
                   "b3lyp_tm", "b3lyp_g"]

    for f1, f2, f3, f4 in grouper(4, functionals):
        f1h, f2h, f3h, f4h = f1+".inp", f2+".inp", f3+".inp", f4+".inp"
        jobhandle = "{0}+{1}+{2}+{3}.pbs".format(f1, f2, f3, f4)

    for functional in functionals:
        orcahandle = functional + ".inp"
        jobhandle  = functional + ".pbs"
        orcafile = open(orcahandle, "w")
        jobfile  = open(jobhandle, "w")

        print >> orcafile, eprfile(charge, xname, functional)
        print >> jobfile,  pbsfile(xname, functional)

        sp.call("qsub {}".format(jobhandle), shell=True)

        orcafile.close()
        jobfile.close()
