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

    When dumping COVPs to cube files, the ordering is:
    1. fragment 1 occupied        (len: f1 occ)
    2. fragment 2 occupied        (len: f2 occ)
    3. fragment 2 virtual         (len: f2 occ)
    4. ??? (remainder of f. virt) (len: f2 occ)
    5. fragment 1 virtual         (len: f1 occ)
    6. ??? (remainder of f. virt) (len: ???)
    '''
    num_frag1_occ = len(fragment_1_to_2)
    num_frag2_occ = len(fragment_2_to_1)
    f1_occ_lo = 1
    f1_occ_hi = f1_occ_lo + num_frag1_occ
    f2_occ_lo = f1_occ_hi
    f2_occ_hi = f2_occ_lo + num_frag2_occ
    f2_virt_lo = f2_occ_hi
    f2_virt_hi = f2_virt_lo + num_frag2_occ
    s1_lo = f2_virt_hi
    s1_hi = s1_lo + num_frag2_occ
    f1_virt_lo = s1_hi
    f1_virt_hi = f1_virt_lo + num_frag1_occ
    s2_lo = f1_virt_hi
    s2_hi = s2_lo
    print('f1 occ:')
    print(list(range(f1_occ_lo, f1_occ_hi)))
    print('f2 occ:')
    print(list(range(f2_occ_lo, f2_occ_hi)))
    print('f2 virt:')
    print(list(range(f2_virt_lo, f2_virt_hi)))
    print('???')
    print(list(range(s1_lo, s1_hi)))
    print('f1 virt:')
    print(list(range(f1_virt_lo, f1_virt_hi)))
    print('???')
    print(list(range(s2_lo, s2_hi)))
    for entry in fragment_1_to_2:
        entry['orb_occ'] = entry['index']
        entry['orb_virt'] = entry['orb_occ'] + num_frag1_occ + (3 * num_frag2_occ)
    for entry in fragment_2_to_1:
        entry['orb_occ'] = entry['index'] + num_frag1_occ
        entry['orb_virt'] = entry['orb_occ'] + num_frag2_occ


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
        # Plot every COVP within the de% cutoff.
        with open('vmd.load_fragment_1_to_2', 'w') as f12_file:
            vmd_covp_write_file(f12_file, xyzfilename, fragment_1_to_2_pairs)
        with open('vmd.load_fragment_2_to_1', 'w') as f21_file:
            vmd_covp_write_file(f21_file, xyzfilename, fragment_2_to_1_pairs)
