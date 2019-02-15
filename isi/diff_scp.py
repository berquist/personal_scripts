#!/usr/bin/env python

import difflib
from pathlib import Path
from typing import List, Tuple


def getargs():
    import argparse
    parser = argparse.ArgumentParser()
    arg = parser.add_argument
    arg("scp1", type=Path)
    arg("scp2", type=Path)
    return parser.parse_args()


def get_scp_lines(scp_filename) -> Tuple[List[str], List[str]]:
    with open(scp_filename) as handle:
        lines = handle.readlines()
    splitlines = [line.split() for line in lines]
    # Try and extract IDs and offsets from the file; offsets may not be
    # available.
    ids = [splitline[0] for splitline in splitlines]
    try:
        offsets = [splitline[1].split(":")[1] for splitline in splitlines]
    except IndexError:
        offsets = []
    return ids, offsets
    


def diff_scp_lines(filename_scp1, filename_scp2):

    ids1, offsets1 = get_scp_lines(filename_scp1)
    ids2, offsets2 = get_scp_lines(filename_scp2)

    diff_ids = list(difflib.unified_diff(ids1, ids2))
    diff_offsets = []
    if offsets1 and offsets2:
        diff_offsets = list(difflib.unified_diff(offsets1, offsets2))

    if diff_ids or diff_offsets:
        return False
    return True


if __name__ == "__main__":
    args = getargs()
    print(diff_scp_lines(args.scp1, args.scp2))
