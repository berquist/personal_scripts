#!/usr/bin/env python

from __future__ import print_function

import argparse


parser = argparse.ArgumentParser()
parser.add_argument('namein')
args = parser.parse_args()
namein = args.namein

inhandle = open(namein)
temp = inhandle.readlines()
print(len(temp))
