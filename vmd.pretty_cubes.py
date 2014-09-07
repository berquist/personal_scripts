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

# RB note:
# Steps 2 and 3 can also be performed by launching vmd from the shell like this: vmd file.xyz -e load_all_plt.vmd
# Step 6: convert.bash script requires Imagemagick convert utility. For Mac OS X, install through Homebrew: brew install imagemagick

"""Help generate a series of pretty pictures from cube files via VMD.

"""

import argparse
import os
from glob import glob


ifmt = 'cube'
ofmt = 'png'

out = 'load_all_plt.vmd'
plot = 'plot_all.vmd'
# conv = 'convert.bash'
html = 'vmd_plots.html'
povrayscript = 'povray.bash'
ncol = 4

parser = argparse.ArgumentParser()
parser.add_argument('--nsurf', choices=[1, 2, 3], default=3, type=int)
parser.add_argument('--maxiso', nargs='?', type=float)
args = parser.parse_args()

nsurf = args.nsurf
maxiso = args.maxiso

# if the maximum isosurface value isn't set, define it based on the number
# of desired surfaces:
if not maxiso:
    if nsurf == 2:
        maxiso = 0.01
    elif nsurf == 3:
        maxiso = 0.0128

outfile = open(out, 'wb')
plotfile = open(plot, 'wb')
# convfile = open(conv, 'wb')
htmlfile = open(html, 'wb')
povrayfile = open(povrayscript, 'wb')

# set the appropriate isovalues
if nsurf == 2:
    print('Using 2 surfaces for isovalues:')
    # an isovalue of 0.99 will produce no surface
    isov = [maxiso, maxiso/8.0, 0.99]
    print(isov[0], isov[1])
elif nsurf == 3:
    print('Using 3 surfaces for isovalues:')
    isov = [maxiso, maxiso/4.0, maxiso/16.0]
    print(isov[0], isov[1], isov[2])

# set opacity and diffuseness based on the number of isosurfaces
if nsurf == 2:
    outfile.write('material change opacity Glass3 0.15\n')
    outfile.write('material change diffuse Glass3 0.10\n')
elif nsurf == 3:
    outfile.write('material change opacity Glass3 0.40\n')

# write the main portion of the VMD display file
color1id = 23
color2id = 29
vmdrenderfile = '''axes location Off
display projection Orthographic
display rendermode GLSL
display depthcue off
color Display Background white
color Element C gray
menu graphics on
material change diffuse Ghost 0.000000
material change ambient Ghost 0.300000
material change opacity Ghost 0.100000
material change shininess Ghost 0.000000
mol addrep 0
mol addrep 0
mol addrep 0
mol addrep 0
mol addrep 0
mol addrep 0
mol modstyle 0 0 Licorice 0.200000 100.000000 100.000000
mol modmaterial 0 0 HardPlastic
mol modmaterial 1 0 HardPlastic
mol modmaterial 2 0 HardPlastic
mol modmaterial 3 0 Glass3
mol modmaterial 4 0 Glass3
mol modmaterial 5 0 Ghost
mol modmaterial 6 0 Ghost
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
'''.format(isov1=isov[0], isov2=isov[1], isov3=isov[2],
           color1=color1id, color2=color2id)
outfile.write(vmdrenderfile)

# convfile.write('#!/bin/bash\n\n')
povrayfile.write('#!/bin/bash\n\n')
# os.chmod(conv, 0755)
os.chmod(povrayscript, 0755)

htmlfile.write('<html>\n<head></head>\n<body>\n')
htmlfile.write('<table>\n<tr>\n')

N = 0
for I in sorted(glob('*{}'.format(ifmt))):

    vmdrenderfile = '''mol addfile {}\n'''.format(I)
    outfile.write(vmdrenderfile)

    # generate the POV-Ray input files
    povray_string_template = 'povray +W{{width}} +H{{height}} -I{{filename}}.pov -O{{filename}}.pov.{ofmt} -D +X +C +A +AM2 +R9 +FN10 +UA +Q11'.format(ofmt=ofmt)
    povray_string = povray_string_template.format(width='%w', height='%h', filename='%s')
    render_options_string = 'render options POV3 "{povray_string}"'.format(povray_string=povray_string)
    vmdplotfile = '''
mol modstyle 1 0 Isosurface  {isov1} {N} 0 0 1 1
mol modstyle 2 0 Isosurface -{isov1} {N} 0 0 1 1
mol modstyle 3 0 Isosurface  {isov2} {N} 0 0 1 1
mol modstyle 4 0 Isosurface -{isov2} {N} 0 0 1 1
mol modstyle 5 0 Isosurface  {isov3} {N} 0 0 1 1
mol modstyle 6 0 Isosurface -{isov3} {N} 0 0 1 1
{render_options_string}
render POV3 {I}.pov
'''.format(I=I, N=N, ofmt=ofmt,
           isov1=isov[0], isov2=isov[1], isov3=isov[2],
           render_options_string=render_options_string)
    plotfile.write(vmdplotfile)

#     imageconvfile = '''
# convert {I}.pov.{ofmt} {I}.png
# rm {I}.{ofmt}
# '''.format(I=I, ofmt=ofmt)
#     convfile.write(imageconvfile)

    htmlentry = '''<td><img src=\"{I}.png\" border=\"1\" width=\"400\">
{I}<br></td>
'''.format(I=I)
    htmlfile.write(htmlentry)

    N += 1
    if (N % ncol) == 0:
        htmlfile.write('</tr><tr>\n')

htmlfile.write('</tr></table>\n')
htmlfile.write('</body>\n</html>\n')

outfile.close()
plotfile.close()
# convfile.close()
htmlfile.close()
povrayfile.close()

print('... finished.')
