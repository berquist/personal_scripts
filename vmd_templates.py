#!/usr/bin/env python

from __future__ import print_function


def vmd_covp_base_template():
    return '''
# general display and rendering settings
display antialias on
display depthcue off
display culling off
display rendermode GLSL
display projection orthographic
display resize 1050 1050
axes location off
menu graphics on

# general color settings
color Element C gray
color Axes Labels black
color Display Background white

# create a new material
material add copy GlassBubble
material rename Material22   GlassBubble2
material change ambient      GlassBubble2 0.000000
material change diffuse      GlassBubble2 1.000000
material change specular     GlassBubble2 1.000000
material change shininess    GlassBubble2 1.000000
material change opacity      GlassBubble2 0.380000
material change outline      GlassBubble2 0.890000
material change outlinewidth GlassBubble2 0.000000
material change transmode    GlassBubble2 1.000000
'''


def vmd_covp_load_xyzfile(xyzfilename):
    color1 = 23 # blue2
    color2 = 30 # red3
    color3 = 21 # cyan2
    color4 = 13 # mauve
    return '''
# load the base XYZ file
mol new {{{xyzfilename}}} type {{xyz}} first 0 last -1 step 1 waitfor 1
mol modcolor 0 0 Element
mol modmaterial 0 0 HardPlastic
mol modstyle 0 0 CPK 1.000000 0.300000 100.000000 100.000000

# add representations for 4 isosurfaces: 1 COVP, 2 phases (opposite sign)
mol addrep 0
mol addrep 0
mol addrep 0
mol addrep 0

mol modstyle 1 0 Isosurface  0.05 0 0 0 1 1
mol modstyle 2 0 Isosurface -0.05 0 0 0 1 1
mol modstyle 3 0 Isosurface  0.05 0 0 0 1 1
mol modstyle 4 0 Isosurface -0.05 0 0 0 1 1

mol modcolor 1 0 ColorID {color1}
mol modcolor 2 0 ColorID {color2}
mol modcolor 3 0 ColorID {color3}
mol modcolor 4 0 ColorID {color4}

mol modmaterial 1 0 GlassBubble2
mol modmaterial 2 0 GlassBubble2
mol modmaterial 3 0 GlassBubble2
mol modmaterial 4 0 GlassBubble2

'''.format(color1=color1, color2=color2, color3=color3, color4=color4,
           xyzfilename=xyzfilename)


## parameters for pair {moidx1}, {moidx2}
#mol new {{mo.{moidx1}.cube}} type {{cube}} first 0 last -1 step 1 waitfor 1 volsets {{0 }}
#mol new {{mo.{moidx2}.cube}} type {{cube}} first 0 last -1 step 1 waitfor 1 volsets {{0 }}


def vmd_covp_pair_load(moidx1, moidx2, vmdidx1, vmdidx2):
    return '''
mol addfile mo.{moidx1}.cube
mol addfile mo.{moidx2}.cube
'''.format(moidx1=moidx1,
           moidx2=moidx2,
           vmdidx1=vmdidx1,
           vmdidx2=vmdidx2)


def vmd_covp_pair_render(moidx1, moidx2, vmdidx1, vmdidx2):
    return '''
mol modstyle 1 0 Isosurface  0.05 {vmdidx1} 0 0 1 1
mol modstyle 2 0 Isosurface -0.05 {vmdidx1} 0 0 1 1
mol modstyle 3 0 Isosurface  0.05 {vmdidx2} 0 0 1 1
mol modstyle 4 0 Isosurface -0.05 {vmdidx2} 0 0 1 1
render TachyonInternal COVP_{moidx1}_{moidx2}.tga
'''.format(moidx1=moidx1,
           moidx2=moidx2,
           vmdidx1=vmdidx1,
           vmdidx2=vmdidx2)


def vmd_covp_write_file_load(loadfile, xyzfilename, mo_pairs, width):
    loadfile.write(vmd_covp_base_template())
    loadfile.write(vmd_covp_load_xyzfile(xyzfilename))
    for idx, mo_pair in enumerate(mo_pairs):
        moidx1 = pad_left_zeros(mo_pair[0], width)
        moidx2 = pad_left_zeros(mo_pair[1], width)
        vmdidx1 = (2 * idx)
        vmdidx2 = vmdidx1 + 1
        loadfile.write(vmd_covp_pair_load(moidx1, moidx2, vmdidx1, vmdidx2))


def vmd_covp_write_file_render(renderfile, mo_pairs, width):
    for idx, mo_pair in enumerate(mo_pairs):
        moidx1 = pad_left_zeros(mo_pair[0], width)
        moidx2 = pad_left_zeros(mo_pair[1], width)
        vmdidx1 = (2 * idx)
        vmdidx2 = vmdidx1 + 1
        renderfile.write(vmd_covp_pair_render(moidx1, moidx2, vmdidx1, vmdidx2))


def vmd_covp_write_files(loadfile, renderfile, xyzfilename, mo_pairs, width):
    loadfile.write(vmd_covp_base_template())
    loadfile.write(vmd_covp_load_xyzfile(xyzfilename))
    for idx, mo_pair in enumerate(mo_pairs):
        moidx1 = pad_left_zeros(mo_pair[0], width)
        moidx2 = pad_left_zeros(mo_pair[1], width)
        vmdidx1 = (2 * idx)
        vmdidx2 = vmdidx1 + 1
        loadfile.write(vmd_covp_pair_load(moidx1, moidx2, vmdidx1, vmdidx2))
        renderfile.write(vmd_covp_pair_render(moidx1, moidx2, vmdidx1, vmdidx2))


def pad_left_zeros(num, maxwidth):
    '''
    '''
    numwidth = len(str(num))
    if numwidth < maxwidth:
        numzeros = maxwidth - numwidth
        numstr = (numzeros * '0') + str(num)
    else:
        numstr = str(num)
    return numstr


if __name__ == '__main__':

    pass
