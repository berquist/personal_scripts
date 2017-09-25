#!/bin/bash

rm -r *.0 Frg* rem* input0 molecule zmat* tmp*
mv plots/*
rmdir plots
qchem_rename_cubes.py
