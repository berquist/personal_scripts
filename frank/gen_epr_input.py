#!/usr/bin/env python2

def eprfile(charge, xyzfile):
    """
    """
    return """! uks pbe0 def2-tzvpp def2-tzvpp/jk ri rijk pmodel somf(1x) noautostart tightscf grid5

%pal
 nprocs 8
 end

* xyzfile {0} 2 {1}.xyz *

%eprnmr
 tol 1e-10
 gtensor 1
 ori -3
 nuclei = all N  {{ aiso, adip, aorb, fgrad, rho }}
 nuclei = all Cu {{ aiso, adip, aorb, fgrad, rho }}
 printlevel 5
 end

""".format(charge, xyzfile)

def eprfile_ptchrg(charge, xyzfile, ptchrgfile):
    """
    """
    return """! uks pbe0 def2-tzvpp def2-tzvpp/jk ri rijk pmodel somf(1x) noautostart tightscf grid5

%pal
 nprocs 8
 end

* xyzfile {0} 2 {1}.xyz *

%pointcharges "{2}.xyz"

%eprnmr
 tol 1e-10
 gtensor 1
 ori -3
 nuclei = all N  {{ aiso, adip, aorb, fgrad, rho }}
 nuclei = all Cu {{ aiso, adip, aorb, fgrad, rho }}
 printlevel 5
 end

""".format(charge, xyzfile, ptchrgfile)

def eprfile_dft(charge, xyzfile, functional):
    """
    """
    return """! uks {2} def2-tzvpp def2-tzvpp/jk ri rijk pmodel somf(1x) noautostart tightscf grid5

%pal
 nprocs 8
 end

* xyzfile {0} 2 {1}.xyz *

%eprnmr
 tol 1e-10
 gtensor 1
 ori -3
 nuclei = all N  {{ aiso, adip, aorb, fgrad, rho }}
 nuclei = all Cu {{ aiso, adip, aorb, fgrad, rho }}
 printlevel 5
 end

""".format(charge, xyzfile, functional)

def pbsfile(xyzfile):
    """
    """
    return """#!/bin/bash

#PBS -N {0}
#PBS -q ishared_large
#PBS -l nodes=1:ppn=8
#PBS -l walltime=144:00:00
#PBS -j oe
#PBS -l qos=low
#PBS -m abe
#PBS -M erb74@pitt.edu

module purge
module load intel/2013.0
module load openmpi/1.6.5-intel12
module load orca/3.0.1

cp $PBS_O_WORKDIR/{0}.inp $LOCAL
cp $PBS_O_WORKDIR/{0}.xyz $LOCAL
cd $LOCAL

run_on_exit() {{
    set -v
    cp $LOCAL/* $PBS_O_WORKDIR
}}

trap run_on_exit EXIT

$(which orca) {0}.inp >& $PBS_O_WORKDIR/{0}.out
""".format(xyzfile)

def pbsfile_ptchrg(xyzfile, ptchrgfile):
    """
    """
    return """#!/bin/bash

#PBS -N {0}
#PBS -q ishared_large
#PBS -l nodes=1:ppn=8
#PBS -l walltime=144:00:00
#PBS -j oe
#PBS -l qos=low
#PBS -m abe
#PBS -M erb74@pitt.edu

module purge
module load intel/2013.0
module load openmpi/1.6.5-intel12
module load orca/3.0.1

cp $PBS_O_WORKDIR/{0}.inp $LOCAL
cp $PBS_O_WORKDIR/{0}.xyz $LOCAL
cp $PBS_O_WORKDIR/{1}.xyz $LOCAL
cd $LOCAL

run_on_exit() {{
    set -v
    cp $LOCAL/* $PBS_O_WORKDIR
}}

trap run_on_exit EXIT

$(which orca) {0}.inp >& $PBS_O_WORKDIR/{0}.out
""".format(xyzfile, ptchrgfile)

def pbsfile_dft(xyzfile, functional):
    """
    """
    return """#!/bin/bash

#PBS -N {1}
#PBS -q ishared_large
#PBS -l nodes=1:ppn=8
#PBS -l walltime=24:00:00
#PBS -j oe
#PBS -m abe
#PBS -M erb74@pitt.edu

module purge
module load intel/2013.0
module load openmpi/1.6.5-intel12
module load orca/3.0.1

cp $PBS_O_WORKDIR/{1}.inp $LOCAL
cp $PBS_O_WORKDIR/{0}.xyz $LOCAL
cd $LOCAL

run_on_exit() {{
    set -v
    cp $LOCAL/* $PBS_O_WORKDIR
}}

trap run_on_exit EXIT

$(which orca) {1}.inp >& $PBS_O_WORKDIR/{1}.out
""".format(xyzfile, functional)

if __name__ == "__main__":
    import argparse
    import subprocess as sp
    import os

    parser = argparse.ArgumentParser(description="")
    parser.add_argument(dest="action", metavar="<action>", type=str, help="")
    parser.add_argument(dest="xname", metavar="<xyzfile>", type=str, help="", nargs="+")
    parser.add_argument("--ptchrgfile", dest="pname", metavar="<ptchrgfile>", type=str, default=None, help="")
    parser.add_argument("--charge", dest="charge", metavar="<charge>", type=int, default=0, help="")
    args = parser.parse_args()

    xnamelist = args.xname
    pname = args.pname
    action = args.action
    charge = args.charge

    # if pname is None:
    #     print >> orcafile, eprfile(charge, xname)
    #     print >> jobfile,  pbsfile(charge, xname)

    # else:
    #     print >> orcafile, eprfile_ptchrg(charge, xname, pname)
    #     print >> jobfile,  pbsfile_ptchrg(charge, xname, pname)

    # orcafile.close()
    # jobfile.close()

    # sp.call(["echo", jobhandle])
    # sp.call(["qsub", jobhandle])

    def gen(xyzfile, ptchrgfile=None, charge=0):
        orcahandle = xyzfile + ".inp"
        jobhandle  = xyzfile + ".pbs"
        orcafile = open(orcahandle, "w")
        jobfile  = open(jobhandle,  "w")

        if ptchrgfile is None:
            print >> orcafile, eprfile(charge, xyzfile)
            print >> jobfile,  pbsfile(xyzfile)

        else:
            print >> orcafile, eprfile_ptchrg(charge, xyzfile, ptchrgfile)
            print >> jobfile,  pbsfile_ptchrg(xyzfile, ptchrgfile)

        orcafile.close()
        jobfile.close()

    def sub(xyzfile, ptchrgfile=None, charge=0):
        gen(xyzfile, ptchrgfile, charge)
        sp.call(["echo", jobhandle])
        sp.call(["qsub", jobhandle])


    def dft(xyzfile, charge=0):
        functionals = ["hfs", "vwn3", "vwn5", "bp86", "blyp", "olyp", "glyp", "xlyp", "pw91", "mpwpw", "mpwlyp", "pbe", "rpbe", "revpbe", "pwp",
                   "b1lyp", "b3lyp", "o3lyp", "x3lyp", "b1p", "b3p", "b3pw", "pw1pw", "mpw1pw", "mpw1lyp", "pbe0", "pw6b95", "bhandhlyp",
                   "tpss", "tpssh", "m06l", "m06", "m062x"]

        for functional in functionals:
            orcahandle = functional + ".inp"
            jobhandle  = functional + ".pbs"
            orcafile = open(orcahandle, "w")
            jobfile  = open(jobhandle, "w")

            print >> orcafile, eprfile_dft(charge, xyzfile, functional)
            print >> jobfile, pbsfile_dft(xyzfile, functional)

            sp.call("qsub {}".format(jobhandle), shell=True)

            orcafile.close()
            jobfile.close()

    if (action == "gen"):
        for xname in xnamelist:
            gen(xname, pname, charge)
    if (action == "sub"):
        for xname in xnamelist:
            sub(xname, pname, charge)
    if (action == "dft"):
        dft(xname, charge)
