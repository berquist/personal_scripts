#!/usr/bin/env python

"""xyz_rotate_by_angle.py: Tools for rotating coordinates around
Cartesian axes using Euler rotation matrices.
"""

import numpy as np
from math import sin, cos, sqrt
import sys


def rotation(theta):
    """Generate a rotation matrix from theta = (alpha, beta, gamma).
    """
    tx, ty, tz = theta
    cx = cos(tx)
    sx = sin(tx)
    cy = cos(ty)
    sy = sin(ty)
    cz = cos(tz)
    sz = sin(tz)
    # pylint: disable=W0612
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    Ry = np.array([[cy, 0, -sy], [0, 1, 0], [sy, 0, cy]])
    Rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    # return np.dot(Rx, np.dot(Ry, Rz))
    return np.dot(Rz, np.dot(Ry, Rz))


# This is an alternative way of ding it.
# def rotation(theta, R=np.zeros(shape=(3, 3))):
#     """Generate a rotation matrix from theta = (alpha, beta, gamma).
#     """
#     cx, cy, cz = np.cos(theta)
#     sx, sy, sz = np.sin(theta)
#     R.flat = (cx*cz - sx*cy*sz, cx*sz + sx*cy*cz, sx*sy,
#               -sx*cz - cx*cy*sz, -sx*sz + cx*cy*cz,
#               cx*sy, sy*sz, -sy*cz, cy)
#     return R


def rotation_matrix(angle, axis):
    """Generate a rotation matrix for rotating around an axis by a
    certain angle.
    """
    if axis in ['x', 'X']:
        axis = [1.0, 0.0, 0.0]
    elif axis in ['y', 'Y']:
        axis = [0.0, 1.0, 0.0]
    elif axis in ['z', 'Z']:
        axis = [0.0, 0.0, 1.0]
    else:
        axis = [0.0, 0.0, 0.0]

    x = axis[0]
    y = axis[1]
    z = axis[2]

    s = sin(angle)
    c = cos(angle)

    mag = sqrt(x*x + y*y + z*z)

    small = 1.0e-10
    if abs(mag) < small:
        unitmat = [[1.0, 0.0, 0.0],
                   [0.0, 1.0, 0.0],
                   [0.0, 0.0, 1.0]]
        return np.array(unitmat)

    x = x / mag
    y = y / mag
    z = z / mag

    xx = x * x
    yy = y * y
    zz = z * z
    xy = x * y
    yz = y * z
    zx = z * x
    xs = x * s
    ys = y * s
    zs = z * s
    one_c = 1.0 - c

    # pylint: disable=C0326
    rotmat = [[(one_c * xx) + c , (one_c * xy) - zs, (one_c * zx) + ys],
              [(one_c * xy) + zs, (one_c * yy) + c , (one_c * yz) - xs],
              [(one_c * zx) - ys, (one_c * yz) + xs, (one_c * zz) + c ]]

    return np.array(rotmat)


def rotate_structure(structure, theta):
    """Rotate the structure by theta = (alpha, beta, gamma).
    """
    alpha, beta, gamma = theta
    rotmat = np.dot(rotation_matrix(gamma, 'z'),
                    np.dot(rotation_matrix(beta, 'y'),
                           rotation_matrix(alpha, 'x')))
    rotated_structure = []
    # apply the rotation matrix to every atom in the structure
    for atom in structure:
        coords = np.array(atom[1:])
        rotcoords = np.dot(rotmat, coords)
        rotatom = [atom[0]]
        rotatom.extend(list(rotcoords))
        rotated_structure.append(rotatom)
    return rotated_structure


def read_xyz_file(xyzfilename):
    """Reads in an XYZ file.
    """
    atoms = []
    with open(xyzfilename) as xyzfile:
        natoms = int(xyzfile.readline().strip())
        comment = xyzfile.readline().strip()
        for line in xyzfile:
            sline = line.split()
            # pylint: disable=W0141
            sline[1:] = list(map(float, sline[1:]))
            atoms.append(sline)
    return natoms, comment, atoms


def write_xyz_file(natoms, comment, structure, outfilename):
    """Writes out an XYZ file to a file on disk.
    """
    s = '{:3s} {:15.10f} {:15.10f} {:15.10f}'
    with open(outfilename) as outfile:
        outfile.write(str(natoms) + '\n')
        outfile.write(comment + '\n')
        for atom in structure:
            # pylint: disable=W0142
            outfile.write(s.format(*atom) + '\n')


def write_xyz_stdout(natoms, comment, structure):
    """Writes out an XYZ file to standard out.
    """
    s = '{:3s} {:15.10f} {:15.10f} {:15.10f}'
    outfile = sys.stdout
    outfile.write(str(natoms) + '\n')
    outfile.write(comment + '\n')
    for atom in structure:
        # pylint: disable=W0142
        outfile.write(s.format(*atom) + '\n')


def main():
    """Rotate a structure contained in an XYZ file by alpha, beta, and
    gamma (in degrees) around the x, y, and z axes,
    respectively. Writes the rotated structure to stdout.
    """

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('xyzfilename')
    parser.add_argument('--alpha', type=float, default=0.0, help='angle around x')
    parser.add_argument('--beta', type=float, default=0.0, help='angle around y')
    parser.add_argument('--gamma', type=float, default=0.0, help='angle around z')
    args = parser.parse_args()
    xyzfilename = args.xyzfilename
    theta = args.alpha, args.beta, args.gamma

    natoms, comment, structure = read_xyz_file(xyzfilename)
    rotated_structure = rotate_structure(structure, theta)
    write_xyz_stdout(natoms, comment, rotated_structure)

if __name__ == "__main__":

    main()
