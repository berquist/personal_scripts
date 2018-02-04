#!/usr/bin/env python2

import os.path
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("xyzfilename", nargs="+")

args = parser.parse_args()

import pymol
pymol.finish_launching()
from pymol import cmd

for state, xyzfilename in enumerate(args.xyzfilename):
    stub = os.path.splitext(xyzfilename)[0]
    # make sure no nasty characters are lurking in our filename
    cleanname = stub.replace("-", "_")
    cmd.load(xyzfilename, object=cleanname, state=state, quiet=0)
    cmd.enable()
    cmd.bg_color("white")
    # pymol.preset.ball_and_stick(selection="all", mode=1)
    cmd.show("lines")
    # pymol.cmd.ray(width=1280, height=1024, renderer=0)
    # pymol.cmd.set("antialias", 2)
    cmd.set("ray_opaque_background", "off")
    cmd.png(stub + ".png", width=1280, height=1024, quiet=0)
    cmd.reinitialize()

cmd.quit()
