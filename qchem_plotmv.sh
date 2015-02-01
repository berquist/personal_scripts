#!/usr/bin/env bash

rm -r *.0 Frg* rem* input0 molecule zmat* tmp*
mv plots/*
rmdir plots
qchem.rename_cubes.py
