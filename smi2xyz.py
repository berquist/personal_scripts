#!/usr/bin/env python

'''smi2xyz.py: take a batch of SMILES files and generate
3D geometries from them.'''

import argparse
import os
import subprocess


s = 'obabel -ismiles {}.smiles -oxyz -O {}.xyz --gen3d'

parser = argparse.ArgumentParser()
parser.add_argument(dest='filenames', nargs='+')
args = parser.parse_args()
filenames = args.filenames

stubs = list(os.path.splitext(filename)[0] for filename in filenames
             if os.path.splitext(filename)[1] == '.smiles')

for stub in stubs:
    subprocess.call(s.format(stub, stub).split())
