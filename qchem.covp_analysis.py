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
    n_covp_1 = len(fragment_1_to_2)
    n_covp_2 = len(fragment_2_to_1)
    n_covp_t = n_covp_1 + n_covp_2
    n_occ_t = idx_homo + 1
    n_virt_t = n_mo - n_occ_t
    n_orb_t = n_occ_t + n_virt_t
    orbital_indices = parse_energy_block(covpenergies, n_occ_t)
    n_occ_1, n_occ_2, n_virt_1, n_virt_2 = get_n_occ_virt_per_fragment(orbital_indices[0],
                                                                       orbital_indices[1],
                                                                       orbital_indices[2],
                                                                       orbital_indices[3],
                                                                       n_orb_t)
    n_orb_1 = n_occ_1 + n_virt_1
    n_orb_2 = n_occ_2 + n_virt_2
    print('NCOVP1: {:3d} NCOVP2: {:3d} NCOVPT: {:3d}'.format(n_covp_1, n_covp_2, n_covp_t))
    print(' NOcc1: {:3d} NVirt1: {:3d}  NOrb1: {:3d}'.format(n_occ_1, n_virt_1, n_orb_1))
    print(' NOcc2: {:3d} NVirt2: {:3d}  NOrb2: {:3d}'.format(n_occ_2, n_virt_2, n_orb_2))
    print(' NOccT: {:3d} NVirtT: {:3d}  NOrbT: {:3d}'.format(n_occ_t, n_virt_t, n_orb_t))
    assert n_occ_t == n_occ_1 + n_occ_2
    assert n_virt_t == n_virt_1 + n_virt_2
    assert n_orb_t == n_orb_1 + n_orb_2
    for entry in fragment_1_to_2:
        entry['orb_occ'] = entry['index']
        entry['orb_virt'] = entry['index'] + n_occ_1 + n_occ_2 + n_virt_1
    for entry in fragment_2_to_1:
        entry['orb_occ'] = entry['index'] + n_occ_1
        entry['orb_virt'] = entry['index'] + n_occ_1 + n_occ_2


def parse_energy_block(covpenergies, n_occ_t):
    '''
    '''
    energylist = list(covpenergies)
    idx_occ_1 = 0
    idx_virt_2 = n_occ_t
    idx_virt_1 = energylist.index(energylist[idx_occ_1], 1)
    idx_occ_2 = energylist.index(energylist[idx_virt_2])
    return idx_occ_1, idx_occ_2, idx_virt_2, idx_virt_1


def get_n_occ_virt_per_fragment(idx_occ_1, idx_occ_2, idx_virt_2, idx_virt_1, n_mo):
    '''
    '''
    n_occ_1 = idx_occ_2
    n_occ_2 = idx_virt_2 - (n_occ_1)
    n_virt_1 = idx_virt_1 - (n_occ_1 + n_occ_2)
    n_virt_2 = n_mo - (n_occ_1 + n_occ_2 + n_virt_1)
    assert n_occ_1 + n_occ_2 + n_virt_1 + n_virt_2 == n_mo
    return n_occ_1, n_occ_2, n_virt_1, n_virt_2


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
    n_mo = cclib_data.nmo
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
        width = len(str(n_mo))
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
