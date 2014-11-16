#!/usr/bin/env python

def eprfile(charge, multiplicity, xyzfile):
    """
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

if __name__ == "__main__":
    import argparse
    import os.path

    parser = argparse.ArgumentParser()
    parser.add_argument("xname")
    parser.add_argument("--charge", default=0)
    parser.add_argument("--mult", default=2)
    args = parser.parse_args()
    xname = os.path.splitext(args.xname)[0]
    charge = args.charge
    mult = args.mult

    orcahandle = xname + ".in"
    orcafile = open(orcahandle, "w")

    print >> orcafile, eprfile(charge, mult, xname)

    orcafile.close()
