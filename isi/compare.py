#!/usr/bin/env python
# pylint: disable=R1711

import filecmp
import hashlib
from enum import Enum, unique
from pathlib import Path
from typing import List, Tuple, Union

from attr import attrib, attrs
from blessings import Terminal

from diff_scp import diff_scp_lines


def getargs():
    import argparse
    parser = argparse.ArgumentParser()
    arg = parser.add_argument
    arg("dir1", type=Path)
    arg("dir2", type=Path)
    arg("--interleaved", action="store_true")
    arg("--write-files", action="store_true")
    return parser.parse_args()


def strip_common(paths):
    paths_parts = (p.parts for p in paths)
    for i, component in enumerate(zip(*paths_parts)):
        if len(set(component)) > 1:
            break
    return [Path(*p.parts[i:]) for p in paths], i


# def get_files(dirname: Path, common_files: List) -> List[Path]:
#     return [
#         p.resolve()
#         for p in sorted(dirname.glob("*"))
#         if p.is_file() and p.name in common_files
#     ]


def joinpaths(prefix: Path, paths: List[Union[Path, str]]) -> List[Path]:
    return [
        prefix.joinpath(Path(p)).resolve(strict=True)
        for p in paths
    ]


def get_files_recursive(top: Path) -> List[Path]:
    def get_files_recursive_acc(top: Path, files: List[Path]) -> None:
        for f in top.iterdir():
            if f.is_file():
                files.append(f.resolve(strict=True))
            elif f.is_dir():
                get_files_recursive_acc(f.resolve(strict=True), files)
        return
    files = []
    get_files_recursive_acc(top, files)
    return files


def get_common_files_recursive(dir1: Path, dir2: Path) -> Tuple[List[Path], List[Path], List[Path], List[Path]]:
    def get_common_files_recursive_acc(
            dir1: Path, dir2: Path,
            files1: List[Path], files2: List[Path],
            dir1_only: List[Path], dir2_only: List[Path]
    ) -> None:
        dcmp = filecmp.dircmp(dir1, dir2)
        files1.extend(joinpaths(dir1, dcmp.common_files))
        files2.extend(joinpaths(dir2, dcmp.common_files))
        # What to do for directories that aren't in common? Gather all their
        # files.
        for p in joinpaths(dir1, dcmp.left_only):
            if p.is_file():
                dir1_only.append(p)
            elif p.is_dir():
                dir1_only.extend(get_files_recursive(p))
        for p in joinpaths(dir2, dcmp.right_only):
            if p.is_file():
                dir2_only.append(p)
            elif p.is_dir():
                dir2_only.extend(get_files_recursive(p))
        for common_dir in dcmp.common_dirs:
            newdir1 = joinpaths(dir1, [common_dir])[0]
            newdir2 = joinpaths(dir2, [common_dir])[0]
            get_common_files_recursive_acc(newdir1, newdir2, files1, files2, dir1_only, dir2_only)
        return
    files1, files2, dir1_only, dir2_only = [], [], [], []
    get_common_files_recursive_acc(dir1, dir2, files1, files2, dir1_only, dir2_only)
    return files1, files2, dir1_only, dir2_only


def get_digests(filenames: List[Path]) -> List[str]:
    digests = []
    for filename in filenames:
        m = hashlib.md5()
        with open(filename, "rb") as handle:
            m.update(handle.read())
        digests.append(m.hexdigest())
    return digests


@unique
class DiffType(Enum):
    SAME = 0
    SCP_PATHS_DIFFER = 1
    SOMETHING_ELSE_DIFFERS = 2


@attrs
class Diff:
    f1: Path = attrib()
    f2: Path = attrib()
    d1: str = attrib()
    d2: str = attrib()
    diff_type: DiffType = attrib(init=False)

    @diff_type.default
    def init_diff_type(self) -> DiffType:
        if self.d1 != self.d2:
            # If a SCP file, there are internal paths that don't matter. Check
            # them separately.
            if self.f1.suffix == self.f2.suffix == ".scp" and diff_scp_lines(self.f1, self.f2):
                return DiffType.SCP_PATHS_DIFFER
            else:
                return DiffType.SOMETHING_ELSE_DIFFERS
        else:
            return DiffType.SAME


    @staticmethod
    def from_files(f1: Path, f2: Path) -> "Diff":
        d1, d2 = get_digests([f1, f2])
        return Diff(f1, f2, d1, d2)


# def print_diff_files(dcmp) -> None:
#     for name in dcmp.diff_files:
#         print("diff_file %s found in %s and %s" % (name, dcmp.left, dcmp.right))
#     for sub_dcmp in dcmp.subdirs.values():
#         print_diff_files(sub_dcmp)
#     return


def main(dir1: Path, dir2: Path) -> None:
    # For now, only take the common files.
    dircmp = filecmp.dircmp(dir1, dir2)
    files1, files2, dir1_only, dir2_only = get_common_files_recursive(dir1, dir2)

    # For displaying full paths, calculate the needed column width from the
    # longest possible path.
    width1 = max(len(str(p)) for p in files1 + dir1_only)
    width2 = max(len(str(p)) for p in files2 + dir2_only)

    t = Terminal()

    map_diff_to_color = {
        DiffType.SAME: t.green,
        DiffType.SCP_PATHS_DIFFER: t.cyan,
        DiffType.SOMETHING_ELSE_DIFFERS: t.red,
    }

    diffs = []
    for f1, f2 in zip(files1, files2):
        diff = Diff.from_files(f1, f2)
        diffs.append(diff)
        line = f"{diff.d1} {diff.d2} {str(f1):{width1}s} {str(f2):{width2}s}"
        print(map_diff_to_color[diff.diff_type](line))
    # Print the unique files separately. FIXME scope hack using the last diff
    for f1 in dir1_only:
        line = f"{' ' * len(str(diff.d1))} {' ' * len(str(diff.d2))} {str(f1):{width1}s} {' ' * width2}"
        print(t.yellow(line))
    for f2 in dir2_only:
        line = f"{' ' * len(str(diff.d1))} {' ' * len(str(diff.d2))} {' ' * width1} {str(f2):{width2}s}"
        print(t.yellow(line))

    if args.write_files:
        with open("compare_diff.txt", "w") as handle:
            for diff in diffs:
                if diff.diff_type == DiffType.SOMETHING_ELSE_DIFFERS:
                    handle.write(f"{str(diff.f1)} {str(diff.f2)}\n")
        # Write out the unique filenames.
        with open("compare_dir1_only.txt", "w") as handle:
            for f in dir1_only:
                handle.write(f"{str(f)}\n")
        with open("compare_dir2_only.txt", "w") as handle:
            for f in dir2_only:
                handle.write(f"{str(f)}\n")

    return


def main_interleaved(dir1: Path, dir2: Path) -> None:
    return


if __name__ == "__main__":
    args = getargs()
    if args.interleaved:
        main_interleaved(args.dir1, args.dir2)
    else:
        main(args.dir1, args.dir2)
