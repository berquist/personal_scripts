#!/usr/bin/env python

"""find_CO2_frequencies.py: Tools for finding a CO2 molecule in a set
of coordinates and extracting those normal modes from a frequency
calculation which include a significant fraction of CO2
displacement.
"""

from __future__ import print_function

import numpy as np
import numpy.linalg as npl
from itertools import combinations, chain

from cclib.parser import ccopen


def distance(icoords, jcoords):
    """Return the Cartesian distance between two vectors of equal
    length.
    """
    return npl.norm(icoords - jcoords)


def find(haystack, needle):
    """Return the index at which the sequence needle appears in the
    sequence haystack, or -1 if it is not found, using the Boyer-
    Moore-Horspool algorithm. The elements of needle and haystack must
    be hashable.

    >>> find([1, 1, 2], [1, 2])
    1

    """
    h = len(haystack)
    n = len(needle)
    skip = {needle[i]: n - i - 1 for i in range(n - 1)}
    i = n - 1
    while i < h:
        for j in range(n):
            if haystack[i - j] != needle[-j - 1]:
                i += skip.get(haystack[i], n)
                break
        else:
            return i - n + 1
    return -1


def find_all_instances(haystack, needle):
    """Find all instances of the needle in the haystack.
    """
    instances = []
    starting_position = 0
    index = 0
    while index != -1:
        index = find(haystack[starting_position:], needle)
        if index > -1:
            if index not in instances:
                instances.append(starting_position + index)
            starting_position += index + 1
    return instances


def find_CO2_atom_indices(atomnos, atomcoords, bond_CO_min=1.15, bond_CO_max=1.18):
    """Return the all possible first indices belonging to the CO2."""
    # The three possible orderings of the CO2 atomic numbers.
    seq1 = [6, 8, 8]
    seq2 = [8, 6, 8]
    seq3 = [8, 8, 6]
    sequences = (seq1, seq2, seq3)
    # Find all possible starting indices for each of the sequences.
    sequence_candidates = list(chain.from_iterable([find_all_instances(atomnos, sequence)
                                                    for sequence in sequences]))
    # print('sequence candidates: {}'.format(sequence_candidates))
    # If no candidates are found, return a bad index.
    if sequence_candidates == []:
        return -1
    # Make sure the bond distances make sense.
    lengths = []
    length_candidates = []
    for c in sequence_candidates:
        l = []
        pair_indices = set()
        block = [c, c + 1, c + 2]
        pairs = combinations(block, 2)
        for pair in pairs:
            d = distance(atomcoords[pair[0]], atomcoords[pair[1]])
            if d > bond_CO_min and d < bond_CO_max:
                l.append(d)
                pair_indices.add(pair[0])
                pair_indices.add(pair[1])
        lengths.append(l)
        if len(pair_indices) > 0:
            length_candidates.append(min(pair_indices))
    # print('lengths: {}'.format(lengths))
    # print('length candidates: {}'.format(sorted(length_candidates)))
    # Now that we've filtered out by bond length, we don't have any
    # other criteria to filter by. Return the matches.
    return sorted(length_candidates)


def find_CO2_mode_indices(index, vibdisps, thresh=0.85):
    """Return a list of indices corresponding to CO2-dominant modes."""
    modelist = []
    # # Find the starting indices of all possible blocks, not including
    # # the CO2.
    # not_CO2_indices = [i for i in range(0, len(vibdisps[0]), 3)
    #                    if i != index]
    # for modeidx, mode in enumerate(vibdisps):
    #     disp_CO2 = np.sum(np.abs(mode)[index:index + 2])
    #     disp_tot = np.sum(np.abs(mode))
    #     fraction_CO2 = disp_CO2 / disp_tot
    #     # Does this group of three have a larger displacement than any
    #     # other group of three?
    #     for start in not_CO2_indices:
    #         disp_grp = np.sum(np.abs(mode)[start:start + 2])
    #         fraction_grp = disp_grp / disp_tot
    #         if fraction_grp > fraction_CO2:
    #             break
    #     else:
    #         modelist.append(modeidx)
    for modeidx, mode in enumerate(vibdisps):
        disp_CO2 = np.sum(np.abs(mode)[index:index + 3])
        disp_tot = np.sum(np.abs(mode))
        disp_not_CO2 = disp_tot - disp_CO2
        fraction_CO2 = disp_CO2 / disp_tot
        if fraction_CO2 >= thresh:
            # print(disp_CO2, disp_tot, disp_not_CO2, fraction_CO2)
            modelist.append(modeidx)
    return modelist


def main(args):
    """The main routine.

    For each frequency calculation output filename passed in:
    1. find the indices that correspond to a CO2 molecule
    2. look for normal mode displacements where a significant fraction 
    of the total displacement contains CO2
    3. 
    """
    filenames = args.filename
    for filename in filenames:
        job = ccopen(filename)
        data = job.parse()

        print('=' * 78)
        print(filename)

        # If from a geometry optimization, always take the last
        # geometry.
        geometries = data.atomcoords[-1]
        atoms = data.atomnos

        # Find the indices corresponding to the CO2.
        start_indices = find_CO2_atom_indices(atoms, geometries)

        assert isinstance(start_indices, list)

        for start in start_indices:
            # Try and access attributes that would belong to a
            # frequency calculation. If they aren't present, then fail
            # silently.
            try:
                vibfreqs = data.vibfreqs
                vibdisps = data.vibdisps
                geometries = data.atomcoords
                atoms = data.atomnos
                # print('vibfreqs:', len(vibfreqs))
                # print('vibdisps:', vibdisps.shape)
                # print('geometries:', geometries[-1].shape)
                # predicted = (3*geometries[-1].shape[0]) - 6
                # print('3N-6:', (3*geometries[-1].shape[0]) - 6)
                # print('3N-5:', predicted - 1)
                # if len(vibfreqs) < predicted:
                #     print('degeneracy')
                # else:
                #     print('no degeneracy')
                modeindices = find_CO2_mode_indices(start, vibdisps, thresh=args.thresh)
                print(modeindices)
                freqs = [vibfreqs[i] for i in modeindices]
                print(freqs)
            except AttributeError:
                pass

        print('=' * 78)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--thresh', type=float, default=0.50)
    parser.add_argument('filename', nargs='+')
    args = parser.parse_args()

    main(args)
