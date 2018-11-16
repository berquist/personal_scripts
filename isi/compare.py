#!/usr/bin/env python

from typing import List

# import difflib
# import filecmp
import hashlib
from pathlib import Path

from blessings import Terminal

from diff_scp import diff_scp_lines


def getargs():
    import argparse
    parser = argparse.ArgumentParser()
    arg = parser.add_argument
    arg("dir1", type=Path)
    arg("dir2", type=Path)
    return parser.parse_args()


def get_files(dirname: Path) -> List[Path]:
    return list(sorted(p for p in dirname.glob("*") if p.is_file()))


def get_digests(filenames: List[Path]) -> List[str]:
    digests = []
    for filename in filenames:
        m = hashlib.md5()
        with open(filename, "rb") as handle:
            m.update(handle.read())
        digests.append(m.hexdigest())
    return digests


def main(dir1: Path, dir2: Path) -> None:
    files1 = get_files(dir1)
    files2 = get_files(dir2)

    # For displaying full paths, calculate the needed column width from the
    # longest possible path.
    width1 = max(len(str(p)) for p in files1)
    width2 = max(len(str(p)) for p in files2)

    t = Terminal()

    # common = set(p.name for p in files1) | set(p.name for p in files2)

    # print(filecmp.cmpfiles(dir1, dir2, common))

    digests1 = get_digests(files1)
    digests2 = get_digests(files2)

    for d1, d2, f1, f2 in zip(digests1, digests2, files1, files2):
        line = f"{d1} {d2} {str(f1):{width1}s} {str(f2):{width2}s}"
        if d1 != d2:
            # If a SCP file, there are internal paths that don't matter. Check
            # them separately.
            if f1.suffix == f2.suffix == ".scp" and diff_scp_lines(f1, f2):
                print(t.cyan(line))
            else:
                print(t.red(line))
        else:
            print(t.green(line))

    return


if __name__ == "__main__":
    args = getargs()
    main(args.dir1, args.dir2)
