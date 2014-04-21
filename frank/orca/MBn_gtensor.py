#!/usr/bin/env python

import argparse
import subprocess
import os.path

# """MBn_gtensor.py: Given a set of XYZ files that are individual fragments of a system, do a many-body expansion of the g-tensor and compare to the full system."""

# parser = argparse.ArgumentParser()
# parser.add_argument('fxyz', nargs='+')
# args = parser.parse_args()
# args = parser.parse_args(sp.check_output(["ls", "~/calc.epr/mbe/frag\*.xyz"]))
# fxyzlist = args.fxyz
fxyzlist = [
    "/home/dlambrecht/erb74/calc.epr/mbe/frag1.xyz",
    "/home/dlambrecht/erb74/calc.epr/mbe/frag2.xyz",
    "/home/dlambrecht/erb74/calc.epr/mbe/frag3.xyz",
    "/home/dlambrecht/erb74/calc.epr/mbe/frag4.xyz",
    "/home/dlambrecht/erb74/calc.epr/mbe/frag5.xyz",
    "/home/dlambrecht/erb74/calc.epr/mbe/frag6.xyz",
    "/home/dlambrecht/erb74/calc.epr/mbe/frag7.xyz"
]

nmax = len(fxyzlist)

def eprfile(charge, multiplicity, xyzfile):
    """
    A default template for an EPR input file.
    """
    return """! uks pbe0 def2-tzvpp def2-tzvpp/jk ri rijk pmodel somf(1x) noautostart tightscf grid5

%pal
 nprocs 1
 end

* xyzfile {0} {1} {2}.xyz *

%eprnmr
 tol 1e-10
 gtensor 1
 ori centerofelcharge
 printlevel 5
 end

""".format(charge, multiplicity, xyzfile)

def pbsfile(xyzfile):
    """
    A default template for a PBS job file.
    """
    return """#!/bin/bash

#PBS -N {0}
#PBS -q shared
#PBS -l nodes=1:ppn=1
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

# generate the jobs for each of the individual fragments
for fxyz in fxyzlist:
    dir = os.path.dirname(fxyz)
    stub = os.path.splitext(os.path.basename(fxyz))[0]
    xyzhandle = open(fxyz, "r")
    xyzhandle.next()
    charge, multiplicity = xyzhandle.next().split()
    xyzhandle.close()
    orcaname = stub + ".inp"
    pbsname = stub + ".pbs"
    orcahandle = open(os.path.join(dir, orcaname), "w")
    pbshandle = open(os.path.join(dir, pbsname), "w")
    print orcaname
    print >> orcahandle, eprfile(charge, multiplicity, stub)
    print pbsname
    print >> pbshandle, pbsfile(stub)
    orcahandle.close()
    pbshandle.close()
