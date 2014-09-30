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
axes location Off

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
    return '''
# load the base XYZ file
mol new {{{xyzfilename}}} type {{xyz}} first 0 last -1 step 1 waitfor 1
mol modcolor 0 0 Element
mol modmaterial 0 0 HardPlastic
mol modstyle 0 0 CPK 1.000000 0.300000 100.000000 100.000000
'''.format(xyzfilename=xyzfilename)


def vmd_covp_plot_pair(moidx1, moidx2, vmdidx1, vmdidx2):
    return '''
# parameters for pair {moidx1},{moidx2}
mol new {{mo.{moidx1}.cube}} type {{cube}} first 0 last -1 step 1 waitfor 1 volsets {{0 }}
mol new {{mo.{moidx2}.cube}} type {{cube}} first 0 last -1 step 1 waitfor 1 volsets {{0 }}

mol addrep {vmdidx1}
mol addrep {vmdidx1}
mol addrep {vmdidx2}
mol addrep {vmdidx2}

mol modstyle 1 {vmdidx1} Isosurface  0.05 0 0 0 1 1
mol modstyle 2 {vmdidx1} Isosurface -0.05 0 0 0 1 1
mol modstyle 1 {vmdidx2} Isosurface  0.05 0 0 0 1 1
mol modstyle 2 {vmdidx2} Isosurface -0.05 0 0 0 1 1

mol modcolor 1 {vmdidx1} ColorID 23 # blue2
mol modcolor 2 {vmdidx1} ColorID 30 # red3
mol modcolor 1 {vmdidx2} ColorID 21 # cyan2
mol modcolor 2 {vmdidx2} ColorID 13 # mauve

mol modmaterial 1 {vmdidx1} GlassBubble2
mol modmaterial 2 {vmdidx1} GlassBubble2
mol modmaterial 1 {vmdidx2} GlassBubble2
mol modmaterial 2 {vmdidx2} GlassBubble2
'''.format(moidx1=moidx1,
           moidx2=moidx2,
           vmdidx1=vmdidx1,
           vmdidx2=vmdidx2)


def vmd_covp_write_file(vmdfile, xyzfilename, mo_pairs, width):
    vmdfile.write(vmd_covp_base_template())
    vmdfile.write(vmd_covp_load_xyzfile(xyzfilename))
    for idx, mo_pair in enumerate(mo_pairs):
        moidx1 = pad_left_zeros(mo_pair[0], width)
        moidx2 = pad_left_zeros(mo_pair[1], width)
        vmdfile.write(vmd_covp_plot_pair(moidx1, moidx2, (2*idx)+1, (2*idx)+2))


def pad_left_zeros(num, maxwidth):
    '''
    '''
    numwidth = len(str(num))
    if numwidth < maxwidth:
        numzeros = maxwidth - numwidth
        numstr = (numzeros * '0') + str(num)
    return numstr


if __name__ == '__main__':

    import argparse
    # parser = argparse.ArgumentParser()
    # parser.add_argument('xyzfilename')
    # args = parser.parse_args()
    # xyzfilename = args.xyzfilename

    # with open('vmd.load', 'w') as vmdfile:
    #     with open('vmd.render', 'w') as renderfile:
    #         vmdfile.write(vmd_covp_base_template())
    #         vmdfile.write(vmd_covp_load_xyzfile(xyzfilename))
    #         for idx, mo in enumerate(mos):
    #             vmdfile.write(vmd_covp_plot_pair(mo[0], mo[1], (2*idx)+1, (2*idx)+2))
