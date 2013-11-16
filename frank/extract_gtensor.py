#!/usr/bin/env python2

def main():
    pass

if __name__ == "__main__":
    import argparse
    import mmap
    import numpy as np

    parser = argparse.ArgumentParser(description="")
    parser.add_argument(dest="orcaname", metavar="<orca output filename>", nargs="+", type=str, default=None, help="")
    args = parser.parse_args()

    orcaname = args.orcaname

    for name in orcaname:

        orcafile = open(name, "r")
        s = mmap.mmap(orcafile.fileno(), 0, access=mmap.ACCESS_READ)
        searchstr = "ELECTRONIC G-MATRIX"
        startidx = s.find(searchstr)
        s.seek(startidx)

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
        s.read(60)
        xx, xy, xz = s.readline().split()
        yx, yy, yz = s.readline().split()
        zx, zy, zz = s.readline().split()
        
        gmatrix = np.array([[xx, xy, xz],
                            [yx, yy, yz],
                            [zx, zy, zz]], dtype=np.float64)
        
        # this should just be a newline character
        s.readline()

        # gather the component breakdown
        gel     = np.asanyarray(s.readline().split()[1:], dtype=np.float64)
        grmc    = np.asanyarray(s.readline().split()[1:], dtype=np.float64)
        gdso1el = np.asanyarray(s.readline().split()[1:], dtype=np.float64)
        gdso2el = np.asanyarray(s.readline().split()[1:], dtype=np.float64)
        gdsotot = np.asanyarray(s.readline().split()[1:], dtype=np.float64)
        gpso1el = np.asanyarray(s.readline().split()[1:], dtype=np.float64)
        gpso2el = np.asanyarray(s.readline().split()[1:], dtype=np.float64)
        gpsotot = np.asanyarray(s.readline().split()[1:], dtype=np.float64)
        
        # this should just be the dashes separating the sections
        s.readline()
        gtottmp = s.readline().split()[1:]
        delgtmp = s.readline().split()[1:]
        x,  y,  z,  giso  = gtottmp[0], gtottmp[1], gtottmp[2], float(gtottmp[4])
        dx, dy, dz, dgiso = delgtmp[0], delgtmp[1], delgtmp[2], float(delgtmp[4])
        gtensor    = np.array([x,  y,  z], dtype=np.float64)
        delgtensor = np.array([dx, dy, dz], dtype=np.float64)
        
        # "Orientation:"
        s.readline()
        
        gorix = np.asanyarray(s.readline().split()[1:], dtype=np.float64)
        goriy = np.asanyarray(s.readline().split()[1:], dtype=np.float64)
        goriz = np.asanyarray(s.readline().split()[1:], dtype=np.float64)
        gori  = np.array([gorix, goriy, goriz])

        print "{1} {2} {0}".format(name, gtensor, giso)
