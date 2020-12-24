#!/usr/bin/env python2


import os.path
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("xyzfilename", nargs="+")

args = parser.parse_args()


import Avogadro

# mol = Avogadro.molecules.addMolecule()

for xyzfilename in args.xyzfilename:
    molfile = Avogadro.MoleculeFile.readFile(xyzfilename)
    mol = molfile.molecule(0)
    print(type(mol))
    widget = Avogadro.GLWidget(mol)
    widget.setMolecule(mol)
    # Avogadro.GLWidget.setBackground("white")
