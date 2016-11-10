#!/usr/bin/env python

"""pick_random_geometries.py: Pick a bunch of random geometries, with
a range based upon how many snapshots that we have, and move them to a
separate directory.
"""

def pad_left_zeros(num, maxwidth):
    """Pad the given number with zeros on the left until the
    total length is maxwidth, returning it as a string.
    """
    numwidth = len(str(num))
    if numwidth < maxwidth:
        numzeros = maxwidth - numwidth
        numstr = (numzeros * '0') + str(num)
    else:
        numstr = str(num)
    return numstr


def getargs():
    """Get command-line arguments."""

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("--n-qm",
                        type=int,
                        default=1,
                        help="""The number of QM ionic liquid pairs is the rate-limiting factor in
                        our calculations, so limit ourselves to
                        working with one value at a time.""")
    parser.add_argument("--pad",
                        action="store_true",
                        help="""Do the snapshot numbers need to be left-padded with zeros for a
                        total width of 4? If so, specify this flag.""")
    parser.add_argument("--rand-min",
                        type=int,
                        default=1,
                        help="""The lower (inclusive) bound for the random number generator.""")
    parser.add_argument("--rand-max",
                        type=int,
                        default=1001,
                        help="""The upper (inclusive) bound for the random number generator.""")
    parser.add_argument("--num-rand",
                        type=int,
                        default=100,
                        help="""The total number of random numbers (snapshots) to pick.""")
    parser.add_argument("--basedir",
                        default="unused",
                        help="""What directory are all the inputs going to be copied from?""")

    args = parser.parse_args()

    return args

if __name__ == "__main__":
    import random
    import os
    import shutil
    from glob import glob

    args = getargs()

    # Be lazy and hard-code this in. Only choose the [0, 2, 4, 6, 8,
    # 10, 12, 14] point charge values.
    mm_pairs_wanted = range(0, 16, 2)
    fname_input_glob = "drop_{n}_{n_qm}qm_{n_mm}mm*.in".format

    random_integers = []
    while len(random_integers) < args.num_rand:
        randint = random.randint(args.rand_min, args.rand_max)
        if randint not in random_integers:
            random_integers.append(randint)

    if args.pad:
        numlist = [pad_left_zeros(n, 4) for n in random_integers]
    else:
        numlist = random_integers
    filenames = [fname_input_glob(n=n, n_qm=args.n_qm, n_mm=n_mm)
                 for n in numlist
                 for n_mm in mm_pairs_wanted]

    # Make our new directory and move chosen files into it.
    dirname = "random_snapshots"
    try:
        os.mkdir(dirname)
    except FileExistsError:
        pass
    for filename in filenames:
        full_filename = glob("{}/{}".format(args.basedir, filename))[0]
        print(full_filename)
        shutil.copy2(full_filename, dirname)
