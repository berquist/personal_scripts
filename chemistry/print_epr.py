#!/usr/bin/env python3


import os.path

import cclib
import numpy as np
import numpy.linalg as npl
from cclib.io import ccopen


def print_dispatch(outputfile):
    job = ccopen(outputfile)
    program_types = (
        (cclib.parser.adfparser.ADF, print_epr_adf),
        (cclib.parser.daltonparser.DALTON, print_epr_dalton),
        (cclib.parser.orcaparser.ORCA, print_epr_orca),
        (cclib.parser.qchemparser.QChem, print_epr_qchem),
    )
    for (program_type, print_function) in program_types:
        if isinstance(job, program_type):
            d = print_function(outputfile)
    return d


def print_epr_orca(outputfile):

    d = dict()

    # -------------------
    # ELECTRONIC G-MATRIX
    # -------------------

    #  The g-matrix:
    #               2.1766588   -0.0419455    0.0785780
    #              -0.0456024    2.1503399    0.0062106
    #               0.0803984    0.0063831    2.0695626

    #  gel          2.0023193    2.0023193    2.0023193
    #  gRMC         2.0012821    2.0012821    2.0012821
    #  gDSO(1el)    0.0005885    0.0007469    0.0008681
    #  gDSO(2el)   -0.0002227   -0.0002837   -0.0003322
    #  gDSO(tot)    0.0003658    0.0004632    0.0005359
    #  gPSO(1el)    0.0334924    0.2332266    0.3909197
    #  gPSO(2el)   -0.0134555   -0.0947635   -0.1580697
    #  gPSO(tot)    0.0200369    0.1384632    0.2328500
    #            ----------   ----------   ----------
    #  g(tot)       2.0216853    2.1402089    2.2346690 iso=  2.1321877
    #  Delta-g      0.0193660    0.1378897    0.2323497 iso=  0.1298685
    #  Orientation:
    #   X          -0.4921117    0.2594594   -0.8309675
    #   Y          -0.2090765    0.8913857    0.4021425
    #   Z           0.8450521    0.3716348   -0.3844145
    with open(outputfile) as fh:
        for line in fh:

            if "Coordinates of the origin" in line:
                origin = np.array(line.split()[5:8], dtype=float)
                print("origin:", return_eigval_string(origin))

            if "ELECTRONIC G-MATRIX" in line:

                for _ in range(3):
                    line = next(fh)

                xx, xy, xz = next(fh).split()
                yx, yy, yz = next(fh).split()
                zx, zy, zz = next(fh).split()

                g_matrix = np.array([[xx, xy, xz], [yx, yy, yz], [zx, zy, zz]], dtype=float)

                for _ in range(1):
                    line = next(fh)

                g_el = float(next(fh).split()[1])
                g_rmc = float(next(fh).split()[1])
                g_dso_1 = np.array(next(fh).split()[1:], dtype=float)
                g_dso_2 = np.array(next(fh).split()[1:], dtype=float)
                g_dso_t = np.array(next(fh).split()[1:], dtype=float)
                g_pso_1 = np.array(next(fh).split()[1:], dtype=float)
                g_pso_2 = np.array(next(fh).split()[1:], dtype=float)
                g_pso_t = np.array(next(fh).split()[1:], dtype=float)

                for _ in range(1):
                    line = next(fh)

                g_tot_tmp = next(fh).split()[1:]
                del_g_tmp = next(fh).split()[1:]

                g_tot = np.array(g_tot_tmp[:3], dtype=float)
                del_g = np.array(del_g_tmp[:3], dtype=float)
                g_iso = float(g_tot_tmp[4])
                del_g_iso = float(del_g_tmp[4])

                assert (g_dso_1 + g_dso_2).all() == g_dso_t.all()
                assert (g_pso_1 + g_pso_2).all() == g_pso_t.all()
                g_sum = g_rmc * np.ones(3) + g_dso_1 + g_dso_2 + g_pso_1 + g_pso_2
                assert g_sum.all() == del_g.all()

                print("\delta g^{{RMC}}        :  {:12.7f}".format(g_rmc))
                print("\delta g^{GC(1e)}     :", return_eigval_string(g_dso_1))
                print("\delta g^{GC(2e)}     :", return_eigval_string(g_dso_2))
                print("\delta g^{OZ/SOC(1e)} :", return_eigval_string(g_pso_1))
                print("\delta g^{OZ/SOC(2e)} :", return_eigval_string(g_pso_2))
                print("\delta g              :", return_eigval_string(del_g))

                break

    return d


def print_epr_dalton(outputfile):

    d = dict()

    with open(outputfile) as fh:
        for line in fh:

            if "Gauge origin (electronic charge centroid)" in line:
                origin = np.array(line.split()[5:], dtype=float)
                print("origin:", return_eigval_string(origin))

            if "G-shift components (ppm)" in line:

                for _ in range(3):
                    line = next(fh)

                g_rmc_ppm = float(next(fh)[9:16])
                g_gc_1_ppm = dalton_parse_line(next(fh))
                g_gc_2_ppm = dalton_parse_line(next(fh))
                g_oz_soc_1_ppm = dalton_parse_line(next(fh))
                g_oz_soc_2_ppm = dalton_parse_line(next(fh))
                g_tot_ppm = dalton_parse_line(next(fh))

                g_sum_ppm = (
                    g_rmc_ppm * np.eye(3)
                    + g_gc_1_ppm
                    + g_gc_2_ppm
                    + g_oz_soc_1_ppm
                    + g_oz_soc_2_ppm
                )
                # This allows for 1 ppm error in every position.
                assert np.sum(abs(g_tot_ppm - g_sum_ppm)) <= 9.0

                g_rmc_abs = g_rmc_ppm / 1.0e6
                g_gc_1_abs = g_gc_1_ppm / 1.0e6
                g_gc_2_abs = g_gc_2_ppm / 1.0e6
                g_oz_soc_1_abs = g_oz_soc_1_ppm / 1.0e6
                g_oz_soc_2_abs = g_oz_soc_2_ppm / 1.0e6
                g_tot_abs = g_tot_ppm / 1.0e6

                g_gc_1_eigvals_abs = g_eigvals(g_gc_1_abs)
                g_gc_2_eigvals_abs = g_eigvals(g_gc_2_abs)
                g_oz_soc_1_eigvals_abs = g_eigvals(g_oz_soc_1_abs)
                g_oz_soc_2_eigvals_abs = g_eigvals(g_oz_soc_2_abs)
                g_tot_eigvals_abs = g_eigvals(g_tot_abs)

                print("One-electron gauge correction")
                print_matrix_ppm(g_gc_1_ppm)
                print("Two-electron gauge correction")
                print_matrix_ppm(g_gc_2_ppm)
                print("One-electron spin-orbit+orbital-Zeeman contribution")
                print_matrix_ppm(g_oz_soc_1_ppm)
                print("Two-electron spin-orbit+orbital-Zeeman contribution")
                print_matrix_ppm(g_oz_soc_2_ppm)

                print("\delta g^{{RMC}}        :  {:12.7f}".format(g_rmc_abs))
                print("\delta g^{GC(1e)}     :", return_eigval_string(g_gc_1_eigvals_abs))
                print("\delta g^{GC(2e)}     :", return_eigval_string(g_gc_2_eigvals_abs))
                print("\delta g^{OZ/SOC(1e)} :", return_eigval_string(g_oz_soc_1_eigvals_abs))
                print("\delta g^{OZ/SOC(2e)} :", return_eigval_string(g_oz_soc_2_eigvals_abs))
                print("\delta g              :", return_eigval_string(g_tot_eigvals_abs))

                break

    return d


def dalton_parse_line(line):
    """Unpack a '@G' line from a DALTON output into a matrix."""

    # each field is 7 characters long
    xx, yy, zz = line[9:16], line[16:23], line[23:30]
    xy, yx, xz = line[30:37], line[37:44], line[44:51]
    zx, yz, zy = line[51:58], line[58:65], line[65:72]

    arr = np.array([[xx, xy, xz], [yx, yy, yz], [zx, zy, zz]], dtype=float)

    return arr


def g_eigvals(g_matrix):
    """Return the eigenvalues of a g-matrix."""

    return np.sqrt(npl.eigvalsh(np.dot(g_matrix.T, g_matrix)))


def print_epr_qchem(outputfile):
    """"""

    d = dict()

    with open(outputfile) as fh:
        for line in fh:

            if "ECC position:" in line:
                origin = np.array(line.split()[2:], dtype=float)
                print("origin:", return_eigval_string(origin))

            if "Relativistic mass correction" in line:
                g_rmc_ppm = float(next(fh).strip())

            if "One-electron gauge correction" in line:
                xx, xy, xz = next(fh).split()
                yx, yy, yz = next(fh).split()
                zx, zy, zz = next(fh).split()
                g_gc_1_ppm = np.array([[xx, xy, xz], [yx, yy, yz], [zx, zy, zz]], dtype=float)

            if "Two-electron gauge correction" in line:
                xx, xy, xz = next(fh).split()
                yx, yy, yz = next(fh).split()
                zx, zy, zz = next(fh).split()
                g_gc_2_ppm = np.array([[xx, xy, xz], [yx, yy, yz], [zx, zy, zz]], dtype=float)

            if "One-electron spin-orbit+orbital-Zeeman contribution" in line:
                xx, xy, xz = next(fh).split()
                yx, yy, yz = next(fh).split()
                zx, zy, zz = next(fh).split()
                g_oz_soc_1_ppm = np.array([[xx, xy, xz], [yx, yy, yz], [zx, zy, zz]], dtype=float)

            if "Two-electron spin-orbit+orbital-Zeeman contribution" in line:
                xx, xy, xz = next(fh).split()
                yx, yy, yz = next(fh).split()
                zx, zy, zz = next(fh).split()
                g_oz_soc_2_ppm = np.array([[xx, xy, xz], [yx, yy, yz], [zx, zy, zz]], dtype=float)

            if "Total shift" in line:
                xx, xy, xz = next(fh).split()
                yx, yy, yz = next(fh).split()
                zx, zy, zz = next(fh).split()
                g_tot_ppm = np.array([[xx, xy, xz], [yx, yy, yz], [zx, zy, zz]], dtype=float)

            if "cpscfman end" in line:
                break

        g_rmc_abs = g_rmc_ppm / 1.0e6
        g_gc_1_abs = g_gc_1_ppm / 1.0e6
        g_gc_2_abs = g_gc_2_ppm / 1.0e6
        g_oz_soc_1_abs = g_oz_soc_1_ppm / 1.0e6
        g_oz_soc_2_abs = g_oz_soc_2_ppm / 1.0e6
        g_tot_abs = g_tot_ppm / 1.0e6

        g_gc_1_eigvals_abs = g_eigvals(g_gc_1_abs)
        g_gc_2_eigvals_abs = g_eigvals(g_gc_2_abs)
        g_oz_soc_1_eigvals_abs = g_eigvals(g_oz_soc_1_abs)
        g_oz_soc_2_eigvals_abs = g_eigvals(g_oz_soc_2_abs)
        g_tot_eigvals_abs = g_eigvals(g_tot_abs)

        print("One-electron gauge correction")
        print_matrix_ppm(g_gc_1_ppm)
        print("Two-electron gauge correction")
        print_matrix_ppm(g_gc_2_ppm)
        print("One-electron spin-orbit+orbital-Zeeman contribution")
        print_matrix_ppm(g_oz_soc_1_ppm)
        print("Two-electron spin-orbit+orbital-Zeeman contribution")
        print_matrix_ppm(g_oz_soc_2_ppm)

        print("\delta g^{{RMC}}        :  {:12.7f}".format(g_rmc_abs))
        print("\delta g^{GC(1e)}     :", return_eigval_string(g_gc_1_eigvals_abs))
        print("\delta g^{GC(2e)}     :", return_eigval_string(g_gc_2_eigvals_abs))
        print("\delta g^{OZ/SOC(1e)} :", return_eigval_string(g_oz_soc_1_eigvals_abs))
        print("\delta g^{OZ/SOC(2e)} :", return_eigval_string(g_oz_soc_2_eigvals_abs))
        print("\delta g              :", return_eigval_string(g_tot_eigvals_abs))

    return d


def print_epr_adf(outputfilename):
    """Rewrite me?"""

    d = dict()

    for line in outputfile:
        # matches if we are doing a perturbative SO calculation
        if "TOTAL EPR Delta g-matrix (ppt)" in line:
            print(os.path.abspath(outputfilename))
            while "Principal components" not in line:
                line = next(outputfile)
            next(outputfile)
            line = next(outputfile)
            gprin_ppt = np.array(map(float, line.split()))
            gprin_full = (gprin_ppt / 1000) + 2.002319
            print("  ppt: {:>11.3f} {:>11.3f} {:>11.3f}".format(*gprin_ppt))
            print(" full: {:>11.3f} {:>11.3f} {:>11.3f}".format(*gprin_full))
            break
        # matches if we are doing a self-consistent SO calculation
        if "Principal g-values" in line:
            print(os.path.abspath(outputfilename))
            gprin_full = np.array(map(float, line.split()[2:]))
            line = next(outputfile)
            gprin_ppt = np.array(map(float, line.split()[1:])) * 1000
            print("  ppt: {:>11.3f} {:>11.3f} {:>11.3f}".format(*gprin_ppt))
            print(" full: {:>11.3f} {:>11.3f} {:>11.3f}".format(*gprin_full))
            break

    return d


def print_matrix_abs(matrix):
    """Pretty-print a 3x3 matrix."""

    assert matrix.shape == (3, 3)

    t = " {:12.7f} {:12.7f} {:12.7f}".format

    for r in range(3):
        print(t(*matrix[r]))

    return


def print_matrix_ppm(matrix):
    """Pretty-print a 3x3 matrix that's in ppm."""

    assert matrix.shape == (3, 3)

    t = " {:6.0f} {:6.0f} {:6.0f}".format

    for r in range(3):
        print(t(*matrix[r]))

    return


def return_eigval_string(eigvals):
    """"""

    assert eigvals.shape == (3,)

    return " {:12.7f} {:12.7f} {:12.7f}".format(*eigvals)


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("outputfile", nargs="+")

    args = parser.parse_args()

    for outputfile in args.outputfile:
        print(outputfile)
        d = print_dispatch(outputfile)
