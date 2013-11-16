#!/bin/bash

# print out *all* the EPR results
find ~/calc.ecoRI/epr -iname "*.out*" -exec orca_extract.py {} +