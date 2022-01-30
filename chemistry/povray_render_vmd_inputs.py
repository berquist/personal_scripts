#!/usr/bin/env python

"""povray.render_vmd_inputs.py: Write a bash script to render all VMD-generated
POV-Ray files in a directory."""

import argparse
import os
from glob import glob

parser = argparse.ArgumentParser()
parser.add_argument("--quality", choices=["vmd", "lq", "hq"])
args = parser.parse_args()
quality = args.quality

runstring = dict()
# need to silence the display (+D -> -D) so we can run over SSH
runstring["vmd"] = "povray +W{width} +H{height} -I{filename} -O{filename}.tga -D +X +A +FT"
runstring["lq"] = ""
runstring[
    "hq"
] = "povray +W{width} +H{height} -I{filename} -O{filename}.tga -D +X +C +A +AM2 +R9 +FT +UA +Q11"

if not quality:
    quality = "vmd"

convertstring = "convert {filename}.tga {filename}.png"

bashfilename = "povray.bash"
with open(bashfilename, "w") as bashfile:
    bashfile.write("#!/usr/bin/env bash\n\n")
    for povrayinputfilename in sorted(glob("*.pov")):
        print(povrayinputfilename)
        with open(povrayinputfilename) as povrayinputfile:
            for line in povrayinputfile:
                if "try povray" in line:
                    width = line.split()[3][2:]
                    height = line.split()[4][2:]
                    break
        bashfile.write(
            "".join(
                [
                    runstring[quality].format(
                        width=width, height=height, filename=povrayinputfilename
                    ),
                    "\n",
                ]
            )
        )
        bashfile.write("".join([convertstring.format(filename=povrayinputfilename), "\n"]))
os.chmod(bashfilename, 0o755)
