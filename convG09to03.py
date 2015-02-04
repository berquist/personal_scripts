#!/usr/bin/env python

from __future__ import print_function

import os
import sys
import re


try:
    gfile = open(sys.argv[1])
except IndexError:
    print("2010 by Lorenz Blum")
    print("2012 by Eric Berquist")
    print("Makes Gaussian 09 output readable by Molekel 5.4")
    print("Usage: ./convG09toG03 [input] [output]")
    print("Do not forget to give the GFINPUT, GFOLDPRINT and \
    POP= keywords to the Gaussian calculation!")

gfile_contents = gfile.readlines()

for line in gfile_contents:
    re.sub("Gaussian 09", "Gaussian 03", line)
    re.sub("Eigenvalues -- ", "EIGENVALUES -- ", line)
    re.sub("Density Matrix:", "DENSITY MATRIX.", line)
    re.sub(" Atom  AN", "Atom AN", line)
