#!/usr/bin/env python

import difflib
from pathlib import Path
from typing import List, Tuple


def getargs():
    import argparse
    parser = argparse.ArgumentParser()
    arg = parser.add_argument
    arg("seg1", type=Path)
    arg("seg2", type=Path)
    return parser.parse_args()


def get_seg_lines(seg_filename) -> Tuple[List[str], List[str], List[str]]:
    with open(seg_filename) as handle:
        lines = handle.readlines()
    if lines:
        splitlines = [line.split() for line in lines]
        filenames = [Path(splitline[0]).name for splitline in splitlines]
        start_positions = [splitline[1] for splitline in splitlines]
        end_positions = [splitline[2] for splitline in splitlines]
    else:
        filenames = []
        start_positions = []
        end_positions = []
    return filenames, start_positions, end_positions


def diff_seg_lines(filename_seg1, filename_seg2):

    filenames1, start_positions1, end_positions1 = get_seg_lines(filename_seg1)
    filenames2, start_positions2, end_positions2 = get_seg_lines(filename_seg2)

    diff_filenames = list(difflib.unified_diff(filenames1, filenames2))
    diff_start_positions = list(difflib.unified_diff(start_positions1, start_positions2))
    diff_end_positions = list(difflib.unified_diff(end_positions1, end_positions2))

    # if diff_filenames or diff_start_positions or diff_end_positions:
    #     return False
    if diff_filenames:
        # print(diff_filenames)
        return False
    if diff_start_positions:
        # print(diff_start_positions)
        return False
    if diff_end_positions:
        # print(diff_end_positions)
        return False
    return True


if __name__ == "__main__":
    args = getargs()
    print(diff_seg_lines(args.seg1, args.seg2))
