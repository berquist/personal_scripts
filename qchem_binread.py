#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division
import numpy as np
import os
import shutil
import struct

from scripts.dump_bytes import read_binary


def getargs():

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('filename')

    args = parser.parse_args()

    return args


def parse_195_file_normal_mode(filename, args):
    # REAL*8 RMode(3*NATOMS,3*NATOMS)
    # CALL FileMan(FM_WRITE,FILE_NORMAL_MODE,FM_DP,3*3*NATOMS*NATOMS,0,FM_BEG,RMode)

    b = read_binary(filename)

    normal_mode = np.fromstring(b, dtype=float)

    # This will stack the normal modes on top of each other.
    return normal_mode.reshape(-1, 3)


def parse_196_file_normal_mode_number(filename, args):
    # CALL FileMan(FM_WRITE,FILE_NORMAL_MODE_NUMBER,FM_INT,1,0,FM_BEG,NVib)

    b = read_binary(filename)

    nvib = struct.unpack('i', b)[0]

    return nvib


def parse_197_file_redmass(filename, args):
    # REAL*8 RedMass(3*NATOMS)
    # CALL FileMan(FM_WRITE,FILE_REDMASS,FM_DP,3*NATOMS,0,FM_BEG,RedMass)

    b = read_binary(filename)

    redmass = np.fromstring(b, dtype=float)

    return redmass


def parse_198_file_frequency(filename, args):
    # REAL*8 Vib(3*NATOMS)
    # CALL FileMan(FM_WRITE,FILE_FREQUENCY,FM_DP,NAT3,0,FM_BEG,Vib)

    b = read_binary(filename)

    frequency = np.fromstring(b, dtype=float)

    return frequency


def parse_199_file_ir_intens(filename, args):
    # REAL*8 IR_INT(3*NATOMS)
    # CALL FileMan(FM_WRITE,FILE_IR_INTENS,FM_DP,NAT3,0,FM_BEG,IR_INT)

    b = read_binary(filename)

    ir_intens = np.fromstring(b, dtype=float)

    return ir_intens


def parse_200_file_raman_intens(filename, args):
    # REAL*8 SVec(3*NATOMS,3)
    # call FileMan(FM_WRITE,FILE_RAMAN_INTENS,FM_DP,NAT3,0,FM_BEG,SVec(1,2))

    b = read_binary(filename)

    raman_intens = np.fromstring(b, dtype=float)

    return raman_intens


def parse_388_file_normal_to_mwc(filename, args):
    # REAL*8 RMode(3*NATOMS,3*NATOMS)
    # CALL FileMan(FM_WRITE,FILE_NORMAL_TO_MWC,FM_DP,NAT3*NAT3,0,FM_BEG,RMode)

    b = read_binary(filename)

    normal_to_mwc = np.fromstring(b, dtype=float)

    # Do nothing else for now.
    return normal_to_mwc


def parse_389_file_normal_to_cart(filename, args):
    # REAL*8 RMode(3*NATOMS,3*NATOMS)
    # DO 10 I=1,NVib
    #     CALL FileMan(FM_WRITE,FILE_NORMAL_TO_CART,FM_DP,NAT3*NAT3,0,FM_BEG,RMode)

    b = read_binary(filename)

    normal_to_cart = np.fromstring(b, dtype=float)

    # Do nothing else for now.
    return normal_to_cart


if __name__ == '__main__':

    np.set_printoptions(threshold=np.inf)

    args = getargs()

    filename = os.path.abspath(args.filename)
    basename = os.path.basename(filename)

    parsefuncs = [
        ('195', parse_195_file_normal_mode),
        ('196', parse_196_file_normal_mode_number),
        ('197', parse_197_file_redmass),
        ('198', parse_198_file_frequency),
        ('199', parse_199_file_ir_intens),
        ('200', parse_200_file_raman_intens),
        ('388', parse_388_file_normal_to_mwc),
        ('389', parse_389_file_normal_to_cart),
    ]

    for (possible_filename, parsefunc) in parsefuncs:
        if basename.split('.')[0] == possible_filename:
            parse_qchem_binary_file = parsefunc

    print('Parsing Q-Chem binary file: {}'.format(filename))
    r = parse_qchem_binary_file(filename, args)
    print(r)
