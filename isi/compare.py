#!/usr/bin/env python

# import difflib
# import filecmp
import hashlib
from pathlib import Path

from blessings import Terminal

from diff_cmvn import diff_scp_lines


def getargs():
    import argparse
    parser = argparse.ArgumentParser()
    arg = parser.add_argument
    arg("dir1", type=Path)
    arg("dir2", type=Path)
    return parser.parse_args()


def get_digests(filenames):
    digests = []
    for filename in filenames:
        m = hashlib.md5()
        with open(filename, "rb") as handle:
            m.update(handle.read())
        digests.append(m.hexdigest())
    return digests


if __name__ == "__main__":
    args = getargs()

    dir1 = args.dir1
    dir2 = args.dir2
    files1 = [p for p in dir1.glob("*") if p.is_file()]
    files2 = [p for p in dir2.glob("*") if p.is_file()]

    t = Terminal()

    # common = set(p.name for p in files1) | set(p.name for p in files2)

    # print(filecmp.cmpfiles(dir1, dir2, common))

    digests1 = get_digests(files1)
    digests2 = get_digests(files2)

    for d1, d2, f1, f2 in zip(digests1, digests2, files1, files2):
        line = f"{d1} {d2} {f1} {f2}"
        if d1 != d2:
            if f1.suffix == f2.suffix == ".scp" and diff_scp_lines(f1, f2):
                # If a SCP file, there are internal paths that don't
                # matter. Check them separately.
                print(t.cyan(line))
            else:
                print(t.red(line))
        else:
            print(t.green(line))
