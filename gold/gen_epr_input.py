#!/usr/bin/env python2

def eprfile(xyzfile):
    """
    """
    return """! uks pbe0 def2-tzvpp def2-tzvpp/jk ri rijk pmodel somf(1x) noautostart tightscf grid5

%pal
nprocs 8
end

* xyzfile 0 2 {}.xyz *

%eprnmr
 tol 1e-10
 gtensor 1
 ori -3
 nuclei = all N  {{ aiso, adip, aorb, fgrad, rho }}
 nuclei = all Cu {{ aiso, adip, aorb, fgrad, rho }}
 nuclei = all H  {{ aiso, adip, aorb, fgrad, rho }}
 nuclei = all O  {{ aiso, adip, aorb, fgrad, rho }}
 nuclei = all C  {{ aiso, adip, aorb, fgrad, rho }}
 printlevel 5
 end

%method
 z_tol 1e-10
 end
""".format(xyzfile)

def eprfile_ptchrg(xyzfile, ptchrgfile):
    """
    """
    return """! uks pbe0 def2-tzvpp def2-tzvpp/jk ri rijk pmodel somf(1x) noautostart tightscf grid5

%pal
nprocs 8
end

* xyzfile 0 2 {0}.xyz *

%pointcharges "{1}.xyz"

%eprnmr
 tol 1e-10
 gtensor 1
 ori -3
 nuclei = all N  {{ aiso, adip, aorb, fgrad, rho }}
 nuclei = all Cu {{ aiso, adip, aorb, fgrad, rho }}
 nuclei = all H  {{ aiso, adip, aorb, fgrad, rho }}
 nuclei = all O  {{ aiso, adip, aorb, fgrad, rho }}
 nuclei = all C  {{ aiso, adip, aorb, fgrad, rho }}
 printlevel 5
 end

%method
 z_tol 1e-10
 end
""".format(xyzfile, ptchrgfile)

def pbsfile(xyzfile):
    """
    """
    return """#!/bin/bash

#PBS -N {0}
#PBS -q shared
#PBS -l nodes=1:ppn=8
#PBS -l walltime=96:00:00
#PBS -j oe
#PBS -l qos=low

module purge
module load openmpi/1.4.5-gcc45
module load orca/2.9.1

cp $PBS_O_WORKDIR/{0}.inp $LOCAL
cp $PBS_O_WORKDIR/{0}.xyz $LOCAL
cd $LOCAL

run_on_exit() {{
    set -v
    cp $LOCAL/* $PBS_O_WORKDIR
}}

trap run_on_exit EXIT

`which orca` {0}.inp >& $PBS_O_WORKDIR/{0}.out
""".format(xyzfile)

def pbsfile_ptchrg(xyzfile, ptchrgfile):
    """
    """
    return """#!/bin/bash

#PBS -N {0}
#PBS -q shared
#PBS -l nodes=1:ppn=8
#PBS -l walltime=96:00:00
#PBS -j oe
#PBS -l qos=low

module purge
module load openmpi/1.4.5-gcc45
module load orca/2.9.1

cp $PBS_O_WORKDIR/{0}.inp $LOCAL
cp $PBS_O_WORKDIR/{0}.xyz $LOCAL
cp $PBS_O_WORKDIR/{1}.xyz $LOCAL
cd $LOCAL

run_on_exit() {{
    set -v
    cp $LOCAL/* $PBS_O_WORKDIR
}}

trap run_on_exit EXIT

`which orca` {0}.inp >& $PBS_O_WORKDIR/{0}.out
""".format(xyzfile, ptchrgfile)

if __name__ == "__main__":
    import argparse
    import subprocess

    parser = argparse.ArgumentParser(description="")
    parser.add_argument(dest="xname", metavar="<xyzfile>", type=str, default="inpfile.xyz", help="")
    parser.add_argument("--ptchrgfile", dest="pname", metavar="<ptchrgfile>", type=str, default=None, help="")
    args = parser.parse_args()
    xname = args.xname
    pname = args.pname

    orcahandle = xname + ".inp"
    jobhandle  = xname + ".pbs"
    orcafile = open(orcahandle, "w")
    jobfile  = open(jobhandle,  "w")

    if pname is None:
        print >> orcafile, eprfile(xname)
        print >> jobfile,  pbsfile(xname)
        # print "=== " + orcahandle + " ==="
        # print eprfile(xname)
        # print "=== " + jobhandle + " ==="
        # print pbsfile(xname)

    else:
        print >> orcafile, eprfile_ptchrg(xname, pname)
        print >> jobfile,  pbsfile_ptchrg(xname, pname)
        # print "=== " + orcahandle + " ==="
        # print eprfile_ptchrg(xname, pname)
        # print "=== " + jobhandle + " ==="
        # print pbsfile_ptchrg(xname, pname)

    orcafile.close()
    jobfile.close()

    subprocess.call(["echo", jobhandle])
    subprocess.call(["qsub", jobhandle])
