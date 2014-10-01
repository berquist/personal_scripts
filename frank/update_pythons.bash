#!/bin/bash

module purge
module load python/anaconda

conda update --yes conda
conda update --yes anaconda
conda update --yes accelerate

module purge
module load python/anaconda3

conda update --yes conda
conda update --yes anaconda
conda update --yes accelerate

module purge
