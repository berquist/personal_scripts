#!/usr/bin/env bash

module purge
module load python/anaconda2
conda update --yes --all
conda clean --yes -i -l -t -p -s

module purge
module load python/anaconda
conda update --yes --all
conda clean --yes -i -l -t -p -s
