#!/usr/bin/env python

from pathlib import Path

import numpy as np

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--nbasis", type=int)
    parser.add_argument("--nmo", type=int)
    parser.add_argument("--nalpha", type=int)
    parser.add_argument("--nbeta", type=int)
    parser.add_argument("path_to_scratchdir", type=Path)
    args = parser.parse_args()

    nbasis = args.nbasis
    nmo = args.nmo
    nalpha = args.nalpha
    nbeta = args.nbeta
    path_to_scratchdir = args.path_to_scratchdir.resolve()

    nocc_a = nalpha
    nvir_a = nmo - nocc_a
    nocc_b = nbeta
    nvir_b = nmo - nocc_b

    # The ordering is
    # - [nbasis*nmo] alpha coefficients
    # - [nbasis*nmo] beta coefficients
    # - [nmo] alpha eigenvalues
    # - [nmo] beta eigenvalues
    #
    # We don't need the MO coefficients in matrix form, so just dump them as a
    # vector.
    c53 = np.frombuffer((path_to_scratchdir / "53.0").read_bytes(), dtype=np.float64)
    expected_len = (2 * nbasis * nmo) + (2 * nmo)
    actual_len = len(c53)
    assert actual_len >= expected_len
    if actual_len > expected_len:
        print("unexpected size of 53: {} expected {} actual".format(expected_len, actual_len))
    mocoeffs_a = c53[: nbasis * nmo]
    mocoeffs_b = c53[nbasis * nmo : 2 * nbasis * nmo]
    eigvals_a = c53[2 * nbasis * nmo : (2 * nbasis * nmo) + nmo]
    eigvals_b = c53[(2 * nbasis * nmo) + nmo : (2 * nbasis * nmo) + (2 * nmo)]

    with open("occupations.txt", "w") as occupations:
        occupations.write("{} {} {} {}\n".format(nocc_a, nvir_a, nocc_b, nvir_b))
    mocoeffs_a.tofile("mocoeffs_a.txt", sep="\n")
    mocoeffs_b.tofile("mocoeffs_b.txt", sep="\n")
    eigvals_a.tofile("eigvals_a.txt", sep="\n")
    eigvals_b.tofile("eigvals_b.txt", sep="\n")

    # Read in the geometry from FILE_GEOM_ORG (593) and transform it by
    # FILE_ORIENT_MATRIX (6).  This works around the fact that FILE_GEOM_ORG
    # is from before any symmetry manipulations, updated geometries aren't
    # written to disk (or are they? where?), but the rotation matrix is.
    # Maybe better to avoid all of this and run with symmetry off...
    c593 = np.frombuffer((path_to_scratchdir / "593.0").read_bytes(), dtype=np.float64).reshape(
        (-1, 4)
    )
    # c6 = np.frombuffer(
    #     (path_to_scratchdir / "6.0").read_bytes(), dtype=np.float64
    # ).reshape((3, 3))
    atomnos = c593[:, 0].astype(np.int32)
    # coords_rot = c6.dot(c593[:, 1:].T).T
    coords_rot = c593[:, 1:]

    with open("nuclei.txt", "w") as nuclei:
        nuclei.write("{}\n".format(len(atomnos)))
        nuclei.write("\n")
        for i, atomno in enumerate(atomnos):
            nuclei.write(
                "{:23.14e} {:23.14e} {:23.14e} {:4d}\n".format(
                    coords_rot[i, 0], coords_rot[i, 1], coords_rot[i, 2], atomno
                )
            )
