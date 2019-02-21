#!/usr/bin/env python

import argparse

import numpy as np
import scipy.stats.stats as st


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("segments_filename")
    args = parser.parse_args()

    segment_boundaries = np.loadtxt(args.segments_filename, usecols=(2, 3))
    segment_lengths = segment_boundaries[:, 1] - segment_boundaries[:, 0]
    count = len(segment_lengths)
    mean = np.mean(segment_lengths)
    median = np.median(segment_lengths)

    print("num segments read: {:d}".format(count))
    print("total time (h): {:.2f}".format(np.sum(segment_lengths) / 3600))
    print("mean (s): {:.2f}".format(mean))
    print("median (s): {:.2f}".format(median))
    print("skew: {:.2f}".format(st.skew(segment_lengths, bias=True)))
    print("skew [corrected]: {:.2f}".format(st.skew(segment_lengths, bias=False)))
    print("skewtest: {}".format(st.skewtest(segment_lengths)))
    print("kurtosis: {:.2f}".format(st.kurtosis(segment_lengths)))

    # Figure out how many segments would fill the desired number of hours,
    # then round up to the nearest 10k.
    possible_num_hours_segmentations = (100, 300, 500, 1000, 1500, 3000)
    print("=== from mean ===")
    for num_hours in possible_num_hours_segmentations:
        num_segments = int(num_hours * 3600 / mean)
        print("{:d} h: {:d} ({:d}) segments".format(num_hours, round(num_segments, -4), num_segments))
    print("=== from median ===")
    for num_hours in possible_num_hours_segmentations:
        num_segments = int(num_hours * 3600 / median)
        print("{:d} h: {:d} ({:d}) segments".format(num_hours, round(num_segments, -4), num_segments))

    return


if __name__ == "__main__":
    main()
