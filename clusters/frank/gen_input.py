#!/usr/bin/env python

def geomopt_bp86_def2svp(nprocs, xyzfile):
    pass

def freq_bp86_def2svp(nprocs, xyzfile):
    pass

def spe_hf_631g_d(nprocs, xyzfile):
    pass

def spe_pbe0_def2svp(nprocs, xyzfile):
    pass

def spe_pbe0_def2qzvpp(nprocs, xyzfile):
    pass

def epr_pbe0_def2tzvpp(nprocs, xyzfile):
    pass

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


def pbsfile(xyzfile, functional):
    """
    """
    return """#!/bin/bash

#PBS -N {1}
#PBS -q ishared_large
#PBS -l nodes=1:ppn=16
#PBS -l walltime=144:00:00
#PBS -j oe
#PBS -l qos=low

module purge
module load intel/2013.0
module load openmpi/1.6.3-intel13
module load orca/3.0.0

cp $PBS_O_WORKDIR/{1}.inp $LOCAL
cp $PBS_O_WORKDIR/{0}.xyz $LOCAL
cd $LOCAL

run_on_exit() {{
    set -v
    cp $LOCAL/* $PBS_O_WORKDIR
}}

trap run_on_exit EXIT

`which orca` {1}.inp >& $PBS_O_WORKDIR/{1}.out
""".format(xyzfile, functional)

if __name__ == "__main__":
    import argparse
    import subprocess as sp
    import os

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

