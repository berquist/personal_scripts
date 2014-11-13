#!/bin/sh

module purge
module load python/anaconda
conda update --yes conda
conda update --yes anaconda
conda update --yes accelerate
conda clean --yes --tarballs
conda clean --yes --packages
conda clean --yes --lock

module purge
module load python/anaconda3
conda update --yes conda
conda update --yes anaconda
conda update --yes accelerate
conda clean --yes --tarballs
conda clean --yes --packages
conda clean --yes --lock
