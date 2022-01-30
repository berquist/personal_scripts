#!/usr/bin/env python

# Original script by Felix Plasser (http://www.chemical-quantum-images.blogspot.de)
# Modified by Jan-Michael Mewes (http://workadayqc.blogspot.de)
# Converted to Python by Eric Berquist (https://github.com/berquist)
#
# 0. $pointval mo 65-74 (Turbomole), plots (Q-Chem), %plots (ORCA), ...
# 1. call this script (choose 2 or 3 surfaces)
# 2. open the molecular structure file in VMD
# 3. load the .plt/.cube files and some settings
#    - "Load state" load_all_plt.vmd
#    - click "Apply" in "Graphical Representations"
# 4. adjust perspective
# 5. "Load state" plot_all.vmd (play plot_all.vmd)
# 6. Run convert.bash script to convert to PNG if desired

# RB note: Steps 2 and 3 can also be performed by launching vmd from
# the shell like this: vmd file.xyz -e load_all_plt.vmd
# Step 6: convert.bash script requires Imagemagick convert utility.
# For Mac OS X, install through Homebrew: brew install imagemagick

"""Help generate a series of pretty pictures from cube files via VMD.

"""

import argparse
import os
from glob import glob

ifmt = "cube"
ofmt = "tga"

out = "vmd.load_all_plt.vmd"
plot = "vmd.plot_all.vmd"
conv = "vmd.convert.bash"
html = "vmd.plots.html"
ncol = 4

parser = argparse.ArgumentParser()
parser.add_argument("--nsurf", choices=[1, 2, 3], default=3, type=int)
parser.add_argument("--maxiso", nargs="?", type=float)
args = parser.parse_args()

nsurf = args.nsurf
maxiso = args.maxiso

# if the maximum isosurface value isn't set, define it based on the number
# of desired surfaces:
if not maxiso:
    if nsurf == 1:
        maxiso = 0.0128
    elif nsurf == 2:
        maxiso = 0.01
    elif nsurf == 3:
        maxiso = 0.0128

outfile = open(out, "w")
plotfile = open(plot, "w")
convfile = open(conv, "w")
htmlfile = open(html, "w")

# set the appropriate isovalues
print("Using {} surfaces for isovalues:".format(nsurf))
if nsurf == 1:
    # an isovalue of 0.99 will produce no surface
    isov = [maxiso, 0.99, 0.99]
    print(isov[0])
elif nsurf == 2:
    # an isovalue of 0.99 will produce no surface
    isov = [maxiso, maxiso / 8.0, 0.99]
    print(isov[0], isov[1])
elif nsurf == 3:
    isov = [maxiso, maxiso / 4.0, maxiso / 16.0]
    print(isov[0], isov[1], isov[2])

# set opacity and diffuseness based on the number of isosurfaces
if nsurf == 1:
    outfile.write("\n")
elif nsurf == 2:
    outfile.write("material change opacity Glass3 0.15\n")
    outfile.write("material change diffuse Glass3 0.10\n")
elif nsurf == 3:
    outfile.write("material change opacity Glass3 0.40\n")

# write the main portion of the VMD display file
color1id = 23
color2id = 29
vmdrenderfile = """
# -*- mode: tcl -*-
axes location off
display resize 1050 1050
display projection Orthographic
display rendermode GLSL
display depthcue off
color Display Background white
color Element C gray
color Element Cu orange
menu graphics on
material change diffuse Ghost 0.000000
material change ambient Ghost 0.300000
material change opacity Ghost 0.100000
material change shininess Ghost 0.000000

# add representations for up to 6 isosurfaces
mol addrep 0
mol addrep 0
mol addrep 0
mol addrep 0
mol addrep 0
mol addrep 0

mol modcolor 0 0 Element
mol modstyle 0 0 Licorice 0.200000 100.000000 100.000000

mol modstyle 1 0 Isosurface  {isov1} 0 0 0 1 1
mol modstyle 2 0 Isosurface -{isov1} 0 0 0 1 1
mol modstyle 3 0 Isosurface  {isov2} 0 0 0 1 1
mol modstyle 4 0 Isosurface -{isov2} 0 0 0 1 1
mol modstyle 5 0 Isosurface  {isov3} 0 0 0 1 1
mol modstyle 6 0 Isosurface -{isov3} 0 0 0 1 1

mol modcolor 1 0 ColorID {color1}
mol modcolor 2 0 ColorID {color2}
mol modcolor 3 0 ColorID {color1}
mol modcolor 4 0 ColorID {color2}
mol modcolor 5 0 ColorID {color1}
mol modcolor 6 0 ColorID {color2}

mol modmaterial 0 0 HardPlastic
mol modmaterial 1 0 HardPlastic
mol modmaterial 2 0 HardPlastic
mol modmaterial 3 0 Glass3
mol modmaterial 4 0 Glass3
mol modmaterial 5 0 Ghost
mol modmaterial 6 0 Ghost
""".format(
    isov1=isov[0], isov2=isov[1], isov3=isov[2], color1=color1id, color2=color2id
)
outfile.write(vmdrenderfile)

convfile.write("#!/bin/env bash\n")
os.chmod(conv, 0o755)

htmlfile.write("<html>\n<head></head>\n<body>\n")
htmlfile.write("<table>\n<tr>\n")

N = 0
for I in sorted(glob("*{}".format(ifmt))):

    vmdrenderfile = """mol addfile {}\n""".format(I)
    outfile.write(vmdrenderfile)

    vmdplotfile = """
mol modstyle 1 0 Isosurface  {isov1} {N} 0 0 1 1
mol modstyle 2 0 Isosurface -{isov1} {N} 0 0 1 1
mol modstyle 3 0 Isosurface  {isov2} {N} 0 0 1 1
mol modstyle 4 0 Isosurface -{isov2} {N} 0 0 1 1
mol modstyle 5 0 Isosurface  {isov3} {N} 0 0 1 1
mol modstyle 6 0 Isosurface -{isov3} {N} 0 0 1 1
# render POV3 {I}.pov
render TachyonInternal {I}.{ofmt}
""".format(
        I=I, N=N, ofmt=ofmt, isov1=isov[0], isov2=isov[1], isov3=isov[2]
    )
    plotfile.write(vmdplotfile)

    imageconvfile = """
echo "convert {I}.{ofmt} {I}.png"
convert {I}.{ofmt} {I}.png
echo "rm {I}.{ofmt}"
rm {I}.{ofmt}
""".format(
        I=I, ofmt=ofmt
    )
    convfile.write(imageconvfile)

    htmlentry = """<td><img src=\"{I}.png\" border=\"1\" width=\"400\">
{I}<br></td>
""".format(
        I=I
    )
    htmlfile.write(htmlentry)

    N += 1
    if (N % ncol) == 0:
        htmlfile.write("</tr><tr>\n")

htmlfile.write("</tr></table>\n")
htmlfile.write("</body>\n</html>\n")

outfile.close()
plotfile.close()
convfile.close()
htmlfile.close()

print("... finished.")
