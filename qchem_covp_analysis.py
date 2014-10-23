#!/usr/bin/env python

'''Identify the indices of the complementary occupied-virtual pairs (COVPs).

Usage:
  qchem.covp_analysis.py [options] <outputfilename>

Options:
  --pct_cutoff=CUTOFF  Energy percentage cutoff to include an orbital for printing/analysis. [Default: 2]
                       Set this to 0 to see the entire COVP table.
  --plot               Generate VMD scripts to plot COVPs within the energy percentage cutoff.
  --df                 Dump results to JSON and Excel files using Pandas.
  --del                If the orbital is below the cutoff, delete its cube file.
  --print_args         Print the argument block.
'''

from __future__ import print_function

import numpy as np

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
    convention is to say virtual orbitals are on the *opposite* fragment, which
    fits more with the concept of COVPs than canonical orbitals. This is to
    correspond with the "Orbital Energy" block in the output file.

    When dumping COVPs to cube files, the ordering is then:
    [lengths are of actual canonical orbitals]
    1. fragment 1 "occupied"        (len: n_occ_1)
    2. fragment 2 "occupied"        (len: n_occ_2)
    3. fragment 2 "virtual"         (len: n_virt_1)
    4. fragment 1 "virtual"         (len: n_virt_2)
    '''
    # some args implicitly passed show up here...need to fix that
    n_covp_1 = len(fragment_1_to_2)
    n_covp_2 = len(fragment_2_to_1)
    n_covp_t = n_covp_1 + n_covp_2
    n_occ_t = idx_homo + 1
    n_virt_t = n_mo - n_occ_t
    n_orb_t = n_occ_t + n_virt_t
    assert n_orb_t == n_mo
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
    Based on the whole COVP orbital energy block, determine the orbital indices
    where each region starts (fragment 1 or 2, occupied or virtual).

    The start of the occupied block is always the first occupied MO for 1.
    The start of the virtual block is always the first virtual MO for 2 (on 1).

    The first virtual MO for 1 (on 2) can be found in the virtual block.
    The first occupied MO for 2 can be found in the occupied block.
    '''
    energylist = list(covpenergies)
    idx_occ, idx_virt = 0, n_occ_t
    idx_occ_1 = 0
    idx_virt_2_on_1 = n_occ_t
    fragment_1_indices = np.where(covpenergies == covpenergies[idx_occ_1])[0]
    fragment_2_indices = np.where(covpenergies == covpenergies[idx_virt_2_on_1])[0]
    idx_occ_2 = fragment_2_indices[0]
    assert idx_occ_1 == fragment_1_indices[0]
    idx_virt_1_on_2 = fragment_1_indices[1]
    assert idx_virt_2_on_1 == fragment_2_indices[1]
    template = 'idx_occ_1: {} idx_occ_2: {} idx_virt_2: {} idx_virt_1: {}'
    print(template.format(idx_occ_1, idx_occ_2, idx_virt_2_on_1, idx_virt_1_on_2))
    return idx_occ_1, idx_occ_2, idx_virt_2_on_1, idx_virt_1_on_2


def get_n_occ_virt_per_fragment(idx_occ_1, idx_occ_2, idx_virt_2, idx_virt_1, n_mo):
    '''
    Based on the starting indices for each COVP orbital block, determine the
    number of occupied and virtual orbitals for each fragment.
    '''
    n_occ_1 = idx_occ_2
    n_occ_2 = idx_virt_2 - (n_occ_1)
    n_virt_1 = idx_virt_1 - (n_occ_1 + n_occ_2)
    n_virt_2 = n_mo - (n_occ_1 + n_occ_2 + n_virt_1)
    assert n_occ_1 + n_occ_2 + n_virt_1 + n_virt_2 == n_mo
    return n_occ_1, n_occ_2, n_virt_1, n_virt_2


def dump_vmd(fragment_1_to_2_pairs, fragment_2_to_1_pairs, n_mo):
    '''
    Write VMD scripts for plotting.
    '''
    width = len(str(n_mo))
    with open('vmd.covp.load', 'w') as loadfile:
        with open('vmd.covp.render', 'w') as renderfile:
            all_pairs = fragment_1_to_2_pairs + fragment_2_to_1_pairs
            vmd_covp_write_files(loadfile, renderfile, xyzfilename, all_pairs, width)


def dump_pandas(fragment_1_to_2_entries, fragment_2_to_1_entries, prefix):
    '''
    Write results to JSON/Excel files using Pandas.
    '''
    results_1_to_2 = dict()
    results_2_to_1 = dict()
    for entry in fragment_1_to_2_entries:
        results_1_to_2[entry['index']] = entry
    for entry in fragment_2_to_1_entries:
        results_2_to_1[entry['index']] = entry
    results_1_to_2_df = pd.DataFrame(results_1_to_2).transpose()
    results_2_to_1_df = pd.DataFrame(results_2_to_1).transpose()
    results_1_to_2_df.to_json('{}.1_to_2.json'.format(prefix))
    results_2_to_1_df.to_json('{}.2_to_1.json'.format(prefix))
    results_1_to_2_df.to_excel('{}.1_to_2.xls'.format(prefix))
    results_2_to_1_df.to_excel('{}.2_to_1.xls'.format(prefix))


def pad_zeros(num, maxlen):
    '''
    Pad the given number with zeros to left until the total length is maxlen.
    '''
    numstr = str(num)
    numlen = len(numstr)
    if numlen < maxlen:
        numzeros = maxlen - numlen
        padnum = (numzeros * '0') + numstr
        return padnum
    else:
        return numstr


if __name__ == '__main__':

    from docopt import docopt
    import os.path
    from cclib.parser import ccopen
    import os

    args = docopt(__doc__)

    if args['--print_args']:
        print(args)

    if args['--df']:
        # We're going to dump our results to JSON and Excel files.
        import pandas as pd

    outputfilename = args['<outputfilename>']
    stub = os.path.splitext(outputfilename)[0]

    print('-' * 78)
    print(outputfilename)

    # Assume we have an appropriately-named XYZ file.
    xyzfilename = stub + '.xyz'

    # The dE(pair)/dE(total) percentage cutoff for inclusion.
    pct_cutoff = int(args['--pct_cutoff'])

    cclib_job = ccopen(outputfilename)
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
    with open(outputfilename) as outputfile:
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
        # Write VMD scripts for plotting.
        dump_vmd(fragment_1_to_2_pairs, fragment_2_to_1_pairs, n_mo)

    if args['--df']:
        # Write results to JSON/Excel files using Pandas.
        dump_pandas(fragment_1_to_2_cutoff, fragment_2_to_1_cutoff, stub)

    if args['--del']:
        maxlen = 0
        # first, find the maximum length of the number field
        # (from Python objects, not the filesystem)
        fragment_entries = fragment_1_to_2 + fragment_2_to_1
        for entry in fragment_entries:
            newlen = max(len(str(entry['orb_occ'])),
                         len(str(entry['orb_virt'])))
            if newlen > maxlen:
                maxlen = newlen
        template = 'mo.{}.cube'
        for entry in fragment_entries:
            if entry['de_alph_pct'] < pct_cutoff:
                orb_occ = pad_zeros(entry['orb_occ'], maxlen)
                orb_virt = pad_zeros(entry['orb_virt'], maxlen)
                orb_occ_filename = template.format(orb_occ)
                orb_virt_filename = template.format(orb_virt)
                print('Deleting ' + orb_occ_filename)
                print('Deleting ' + orb_virt_filename)
                try:
                    os.remove(orb_occ_filename)
                except OSError:
                    print("Can't remove " + orb_occ_filename)
                try:
                    os.remove(orb_virt_filename)
                except OSError:
                    print("Can't remove " + orb_virt_filename)

    print('-' * 78)
