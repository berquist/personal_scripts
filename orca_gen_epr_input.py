#!/usr/bin/env python

from __future__ import print_function

def eprfile(charge, multiplicity, xyzfile):
    """A default template for running ORCA EPR calculations, finding the
    g-tensor and copper/nitrogen hyperfine/nuclear quadrupole tensors.
    """
    return """! uks pbe0 def2-tzvpp def2-tzvpp/jk ri rijk pmodel somf(1x) noautostart tightscf grid5

%pal
 nprocs 8
 end

* xyzfile {0} {1} {2}.xyz *

%eprnmr
 tol 1e-10
 gtensor 1
 ori -3
 nuclei = all N  {{ aiso, adip, aorb, fgrad, rho }}
 nuclei = all Cu {{ aiso, adip, aorb, fgrad, rho }}
 printlevel 5
 end

""".format(charge, multiplicity, xyzfile)


def eprfile_ptchrg(charge, multiplicity, xyzfile, ptchrgfile):
    """A default template for running ORCA EPR calculations, finding the
    g-tensor and copper/nitrogen hyperfine nuclear quadrupole tensors.

    Perform the calculation in a field of point charges.
    """
    return """! uks pbe0 def2-tzvpp def2-tzvpp/jk ri rijk pmodel somf(1x) noautostart tightscf grid5

%pal
 nprocs 8
 end

* xyzfile {0} {1} {2}.xyz *

%pointcharges "{3}.xyz"

%eprnmr
 tol 1e-10
 gtensor 1
 ori -3
 nuclei = all N  {{ aiso, adip, aorb, fgrad, rho }}
 nuclei = all Cu {{ aiso, adip, aorb, fgrad, rho }}
 printlevel 5
 end

""".format(charge, multiplicity, xyzfile, ptchrgfile)


def eprfile_dft(charge, xyzfile, functional):
    """A default template for running ORCA EPR calculations, finding the
    g-tensor and copper/nitrogen hyperfine nuclear quadrupole tensors.

    Allow changing the density functional used.
    """
    return """! uks {functional} def2-tzvpp def2-tzvpp/jk ri rijk pmodel somf(1x) noautostart tightscf grid5

%pal
 nprocs 8
 end

* xyzfile {charge} {multiplicity} {xyzfile}.xyz *

%eprnmr
 tol 1e-10
 gtensor 1
 ori -3
 nuclei = all N  {{ aiso, adip, aorb, fgrad, rho }}
 nuclei = all Cu {{ aiso, adip, aorb, fgrad, rho }}
 printlevel 5
 end

""".format(charge=charge,
           multiplicity=multiplicity,
           xyzfile=xyzfile,
           functional=functional)


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
        functionals = [
            "hfs",
            "vwn3",
            "vwn5",
            "bp86",
            "blyp",
            "olyp",
            "glyp",
            "xlyp",
            "pw91",
            "mpwpw",
            "mpwlyp",
            "pbe",
            "rpbe",
            "revpbe",
            "pwp",
            "b1lyp",
            "b3lyp",
            "o3lyp",
            "x3lyp",
            "b1p",
            "b3p",
            "b3pw",
            "pw1pw",
            "mpw1pw",
            "mpw1lyp",
            "pbe0",
            "pw6b95",
            "bhandhlyp",
            "tpss",
            "tpssh",
            "m06l",
            "m06",
            "m062x"
        ]

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
