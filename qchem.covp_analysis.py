#!/usr/bin/env python

'''Identify the indices of the complementary occupied-virtual pairs (COVPs).

Usage:
  qchem.covp_analysis.py [options] <outputfilename>

Options:
  --pct_cutoff=CUTOFF  Energy percentage cutoff to include an orbital for printing/analysis. [Default: 2]
  --plot               Generate VMD scripts to plot COVPs within the energy percentage cutoff.
  --print_args         Print the argument block.
'''

from __future__ import print_function

from vmd_templates import *


def parse_fragment_block(outputfile, fragment_entries, fragment_idx):
    '''Parse a single fragment block.'''
    next(outputfile)
    next(outputfile)
    next(outputfile)
    line = next(outputfile)
    while '-----' not in line:
        index = int(line[0:4])
        de_alph = float(line[4:13])
        de_alph_pct = float(line[14:19])
        de_beta = float(line[21:30])
        de_beta_pct = float(line[31:36])
        dq_alph = float(line[38:46])
        dq_alph_pct = float(line[47:52])
        dq_beta = float(line[54:62])
        dq_beta_pct = float(line[63:68])
        entry = {
            'index': index,
            'de_alph': de_alph,
            'de_alph_pct': de_alph_pct,
            'de_beta': de_beta,
            'de_beta_pct': de_beta_pct,
            'dq_alph': dq_alph,
            'dq_alph_pct': dq_alph_pct,
            'dq_beta': dq_beta,
            'dq_beta_pct': dq_beta_pct
        }
        fragment_entries.append(entry)
        line = next(outputfile)


def determine_fragment_indices(fragment_1_to_2, fragment_2_to_1):
    '''
    Determine the actual orbital indices each COVP corresponds to.

    We define an 'occupied' orbital as one charge is being donated from, and
    a 'virtual' orbital as one charge is being donated to.

    Example
    =======
    1 to 2:  1 -> 211
    2 to 1: 42 ->  53

    We consider 1 and 42 as being occupied, and 211 and 53 as being virtual.
    211 and 53 are occupieds belonging to 1 and 2, respectively; this routine's
    convention is to say occupied orbitals are on the *opposite* fragment. This
    is to correspond with the "Orbital Energy" block in the output file.

    When dumping COVPs to cube files, the ordering is then:
    [lengths are of actual canonical orbitals]
    1. fragment 1 "occupied"        (len: NOcc1)
    2. fragment 2 "occupied"        (len: NOcc2)
    3. fragment 2 "virtual"         (len: NVirt1)
    4. fragment 1 "virtual"         (len: NVirt2)
    '''
    NCOVP1 = len(fragment_1_to_2)
    NCOVP2 = len(fragment_2_to_1)
    NCOVPT = NCOVP1 + NCOVP2
    NOccT = idx_homo + 1
    NVirtT = nmo - NOccT
    NOrbT = NOccT + NVirtT
    NOcc1 = NCOVP1
    NOcc2 = NCOVP2
    NVirt1 = find_nvirt1(covpenergies, NOccT)
    NVirt2 = NVirtT - NVirt1
    NOrb1 = NOcc1 + NVirt1
    NOrb2 = NOcc2 + NVirt2
    assert NOccT == NOcc1 + NOcc2
    assert NVirtT == NVirt1 + NVirt2
    assert NOrbT == NOrb1 + NOrb2
    print('NCOVP1: {:3d} NCOVP2: {:3d} NCOVPT: {:3d}'.format(NCOVP1, NCOVP2, NCOVPT))
    print(' NOcc1: {:3d} NVirt1: {:3d}  NOrb1: {:3d}'.format(NOcc1, NVirt1, NOrb1))
    print(' NOcc2: {:3d} NVirt2: {:3d}  NOrb2: {:3d}'.format(NOcc2, NVirt2, NOrb2))
    print(' NOccT: {:3d} NVirtT: {:3d}  NOrbT: {:3d}'.format(NOccT, NVirtT, NOrbT))
    # Keep for posterity:
    # f1_occ_lo = 1
    # f1_occ_hi = NOcc1 + f1_occ_lo
    # f2_occ_lo = f1_occ_hi
    # f2_occ_hi = NOcc2 + f2_occ_lo
    # f2_virt_lo = f2_occ_hi
    # f2_virt_hi = NVirt1 + f2_virt_lo
    # f1_virt_lo = f2_virt_hi
    # f1_virt_hi = NVirt2 + f1_virt_lo
    # print('f1 occ:')
    # print(list(range(f1_occ_lo, f1_occ_hi)))
    # print('f2 occ:')
    # print(list(range(f2_occ_lo, f2_occ_hi)))
    # print('f2 virt:')
    # print(list(range(f2_virt_lo, f2_virt_hi)))
    # print('f1 virt:')
    # print(list(range(f1_virt_lo, f1_virt_hi)))
    for entry in fragment_1_to_2:
        entry['orb_occ'] = entry['index']
        entry['orb_virt'] = entry['index'] + NOcc1 + NOcc2 + NVirt1
    for entry in fragment_2_to_1:
        entry['orb_occ'] = entry['index'] + NOcc1
        entry['orb_virt'] = entry['index'] + NOcc1 + NOcc2


def find_virt_1_index(covpenergies):
    '''
    '''
    energylist = list(covpenergies)
    energy_frag_1_occ = energylist[0]
    # this is obviously not bulletproof...
    idx_virt_1 = energylist.index(energy_frag_1_occ, 1)
    print(idx_virt_1)
    return idx_virt_1


def find_nvirt1(covpenergies, nocc_t):
    '''
    '''
    nvirt_1 = find_virt_1_index(covpenergies) - nocc_t
    return nvirt_1


if __name__ == '__main__':

    from docopt import docopt
    import os.path
    from cclib.parser import ccopen

    args = docopt(__doc__)

    if args['--print_args']:
        print(args)

    # Assume we have an appropriately-named XYZ file.
    xyzfilename = os.path.splitext(args['<outputfilename>'])[0] + '.xyz'

    # The dE(pair)/dE(total) percentage cutoff for inclusion.
    pct_cutoff = int(args['--pct_cutoff'])

    cclib_job = ccopen(args['<outputfilename>'])
    cclib_data = cclib_job.parse()
    nmo = cclib_data.nmo
    idx_homo = cclib_data.homos[0]
    covpenergies = cclib_data.moenergies[-1]

    fragment_1_to_2 = []
    fragment_2_to_1 = []
    fragment_1_to_2_cutoff = []
    fragment_2_to_1_cutoff = []
    fragment_1_to_2_pairs = []
    fragment_2_to_1_pairs = []

    # Parse the COVP fragment print block for each fragment.
    with open(args['<outputfilename>']) as outputfile:
        for line in outputfile:
            if 'From fragment 1 to fragment 2' in line:
                parse_fragment_block(outputfile, fragment_1_to_2, 1)
            if 'From fragment 2 to fragment 1' in line:
                parse_fragment_block(outputfile, fragment_2_to_1, 2)

    # Determine the actual orbital indices each COVP corresponds to.
    determine_fragment_indices(fragment_1_to_2, fragment_2_to_1)

    header = ' idx  occ virt      de   de%     dq   dq%'
    fs = ' {:3d} {:4d} {:4d} {:6} {:5} {:6} {:5}'

    print('Fragment 1 -> 2:')
    print(header)
    for entry in fragment_1_to_2:
        if entry['de_alph_pct'] >= pct_cutoff:
            fragment_1_to_2_cutoff.append(entry)
            fragment_1_to_2_pairs.append((entry['orb_occ'], entry['orb_virt']))
            print(fs.format(entry['index'],
                            entry['orb_occ'],
                            entry['orb_virt'],
                            entry['de_alph'],
                            entry['de_alph_pct'],
                            entry['dq_alph'],
                            entry['dq_alph_pct']))
    print('Fragment 2 -> 1:')
    print(header)
    for entry in fragment_2_to_1:
        if entry['de_alph_pct'] >= pct_cutoff:
            fragment_2_to_1_cutoff.append(entry)
            fragment_2_to_1_pairs.append((entry['orb_occ'], entry['orb_virt']))
            print(fs.format(entry['index'],
                            entry['orb_occ'],
                            entry['orb_virt'],
                            entry['de_alph'],
                            entry['de_alph_pct'],
                            entry['dq_alph'],
                            entry['dq_alph_pct']))

    if args['--plot']:
        width = len(str(nmo))
        # Plot every COVP within the de% cutoff.
        with open('vmd.fragment_1_to_2.load', 'w') as f12_file_load:
            with open('vmd.fragment_1_to_2.render', 'w') as f12_file_render:
                vmd_covp_write_files(f12_file_load,
                                     f12_file_render,
                                     xyzfilename,
                                     fragment_1_to_2_pairs,
                                     width)
        with open('vmd.fragment_2_to_1.load', 'w') as f21_file_load:
            with open('vmd.fragment_2_to_1.render', 'w') as f21_file_render:
                vmd_covp_write_files(f21_file_load,
                                     f21_file_render,
                                     xyzfilename,
                                     fragment_2_to_1_pairs,
                                     width)
