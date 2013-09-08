#!/usr/bin/env python2

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('namein')
args = parser.parse_args()
namein = args.namein

inhandle = open(namein, 'r')
temp = inhandle.readlines()
print len(temp)
