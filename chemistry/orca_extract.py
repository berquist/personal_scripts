#!/usr/bin/env python


def get_coords(orcamap):
    """
    Retrieve all the atoms from an ORCA output file and store them as molecules.
    """
    pass


def get_gtensor(orcamap):

    orcamap.seek(0)
    searchstr = "ELECTRONIC G-MATRIX"
    startidx = orcamap.find(searchstr)
    if startidx == -1:
        return "[]", 0.0
    orcamap.seek(startidx)

    # Here is a sample of what we would like to parse:
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

    # fast-forward a bit and gather the orientation-dependent g-matrix
    orcamap.read(60)
    xx, xy, xz = orcamap.readline().split()
    yx, yy, yz = orcamap.readline().split()
    zx, zy, zz = orcamap.readline().split()

    gmatrix = np.array([[xx, xy, xz], [yx, yy, yz], [zx, zy, zz]], dtype=np.float64)

    # this should just be a newline character
    orcamap.readline()

    # gather the component breakdown
    gel = np.asanyarray(orcamap.readline().split()[1:], dtype=np.float64)
    grmc = np.asanyarray(orcamap.readline().split()[1:], dtype=np.float64)
    gdso1el = np.asanyarray(orcamap.readline().split()[1:], dtype=np.float64)
    gdso2el = np.asanyarray(orcamap.readline().split()[1:], dtype=np.float64)
    gdsotot = np.asanyarray(orcamap.readline().split()[1:], dtype=np.float64)
    gpso1el = np.asanyarray(orcamap.readline().split()[1:], dtype=np.float64)
    gpso2el = np.asanyarray(orcamap.readline().split()[1:], dtype=np.float64)
    gpsotot = np.asanyarray(orcamap.readline().split()[1:], dtype=np.float64)

    # this should just be the dashes separating the sections
    orcamap.readline()
    gtottmp = orcamap.readline().split()[1:]
    delgtmp = orcamap.readline().split()[1:]
    x, y, z, giso = gtottmp[0], gtottmp[1], gtottmp[2], float(gtottmp[4])
    dx, dy, dz, dgiso = delgtmp[0], delgtmp[1], delgtmp[2], float(delgtmp[4])
    gtensor = np.array([x, y, z], dtype=np.float64)
    delgtensor = np.array([dx, dy, dz], dtype=np.float64)

    # "Orientation:"
    orcamap.readline()

    gorix = np.asanyarray(orcamap.readline().split()[1:], dtype=np.float64)
    goriy = np.asanyarray(orcamap.readline().split()[1:], dtype=np.float64)
    goriz = np.asanyarray(orcamap.readline().split()[1:], dtype=np.float64)
    gori = np.array([gorix, goriy, goriz])

    return gtensor, giso


def get_atensor(orcamap):

    orcamap.seek(0)
    searchstr = "CARTESIAN COORDINATES (ANGSTROEM)"
    startidx = orcamap.find(searchstr)
    if startidx == -1:
        return "[]", 0.0, 0.0, 0, 0
    orcamap.seek(startidx)

    # skip over 'CARTESIAN COORDINATES (ANGSTROEM)\n---------------------------------\n'
    orcamap.read(68)
    nitrogens = []
    atomidx = 0
    # from the coordinate block, gather the copper and all the nitrogen atoms
    while True:
        atom = orcamap.readline().split()
        if len(atom) == 0:
            break
        if atom[0] == "Cu":
            cu = np.array([atomidx, atom[1], atom[2], atom[3]], dtype=np.float64)
        if atom[0] == "N":
            n = np.array([atomidx, atom[1], atom[2], atom[3]], dtype=np.float64)
            nitrogens.append(n)
        atomidx += 1

    nitrogenidx = 0
    dist = 999.9
    # find the nitrogen atom that's closest to the copper, that's
    # the one we want hyperfine information for
    for atom in nitrogens:
        copper = cu[1:]
        nitrogen = atom[1:]
        tmpdist = np.linalg.norm(copper - nitrogen)
        if tmpdist < dist:
            dist = tmpdist
            nitrogenidx = atom[0]

    searchstr = str(int(nitrogenidx)) + "N : A"
    orcamap.seek(0)
    startidx = orcamap.find(searchstr)
    if startidx == -1:
        return "[]", 0.0, 0.0, 0, 0
    orcamap.seek(startidx)
    searchstr = "Raw HFC matrix (all values in MHz):"
    startidx = orcamap.find(searchstr)
    if startidx == -1:
        return "[]", 0.0, 0.0, 0, 0
    orcamap.seek(startidx)
    orcamap.readline()

    # next three lines are the raw HFC matrix
    xx, xy, xz = orcamap.readline().split()
    yx, yy, yz = orcamap.readline().split()
    zx, zy, zz = orcamap.readline().split()

    amatrix = np.array([[xx, xy, xz], [yx, yy, yz], [zx, zy, zz]], dtype=np.float64)

    # this should just be a blank line/newline character
    orcamap.readline()

    # gather the component breakdown
    afc = np.array(orcamap.readline().split()[1:], dtype=np.float64)
    asd = np.array(orcamap.readline().split()[1:], dtype=np.float64)
    asotmp = orcamap.readline().split()[1:]
    aso = np.array([asotmp[0], asotmp[1], asotmp[2]], dtype=np.float64)
    apc = float(asotmp[-1])

    # this should just be the dashes separating the sections
    orcamap.readline()

    # get the computed hyperfine tensor
    atottmp = orcamap.readline().split()[1:]
    x, y, z, aiso = atottmp[0], atottmp[1], atottmp[2], float(atottmp[4])
    atensor = np.array([x, y, z], dtype=np.float64)

    # "Orientation:"
    orcamap.readline()

    aorix = np.asanyarray(orcamap.readline().split()[1:], dtype=np.float64)
    aoriy = np.asanyarray(orcamap.readline().split()[1:], dtype=np.float64)
    aoriz = np.asanyarray(orcamap.readline().split()[1:], dtype=np.float64)
    aori = np.array([aorix, aoriy, aoriz])

    return atensor, aiso, dist, int(nitrogenidx), int(atomidx)


def get_atensor_nitrogens():
    pass


if __name__ == "__main__":
    import argparse
    import mmap

    import numpy as np

    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        dest="orcaname",
        metavar="<orca output filename>",
        nargs="+",
        type=str,
        default=None,
        help="",
    )
    args = parser.parse_args()

    orcaname = args.orcaname

    print(
        "{:>34s} {:>10s} {:>28s} {:>10s} {:>10s} {:>4s} {:>6s} {:<s}".format(
            "g-tensor", "isotropic", "a-tensor", "isotropic", "distance", "nidx", "natoms", "name"
        )
    )

    for name in orcaname:

        orcafile = open(name, "r+b")
        orcamap = mmap.mmap(orcafile.fileno(), 0, access=mmap.ACCESS_READ)

        gtensor, giso = get_gtensor(orcamap)
        atensor, aiso, dist, nitrogenidx, natoms = get_atensor(orcamap)

        print(
            "{:>28s} {:>10.7f} {:>28s} {:>10.6f} {:>10.7f} {:>4d} {:>6d} {:<s}".format(
                gtensor, giso, atensor, aiso, dist, nitrogenidx, natoms, name
            )
        )
