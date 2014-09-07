#!/usr/bin/env python

'''povray.render_vmd_inputs.py: Write a bash script to render all VMD-generated
POV-Ray files in a directory.'''

from glob import glob

bashfilename = 'povray.bash'
with open(bashfilename, 'wb') as bashfile:
    bashfile.write('#!/bin/bash\n\n')
    for povrayinputfilename in sorted(glob('*.pov')):
        print(povrayinputfilename)
        with open(povrayinputfilename) as povrayinputfile:
            for line in povrayinputfile:
                if 'try povray' in line:
                    width = line.split()[3][2:]
                    height = line.split()[4][2:]
                    break
        runstring = 'povray +W{width} +H{height} -I{filename} -O{filename}.png -D +X +C +A +AM2 +R9 +FN10 +UA +Q11'
        bashfile.write(''.join([runstring.format(width=width, height=height, filename=povrayinputfilename), '\n']))
