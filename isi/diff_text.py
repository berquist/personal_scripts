import difflib
import sys
from collections import Counter


def make_counts(filename):
    tokens = []
    with open(filename) as handle:
        for line in handle:
            tokens.extend(line.split()[1:])
    return Counter(tokens)
            

if __name__ == "__main__":


    filename_left = "/nas/material/users/berquist/expts/m0004/16k_som_exp/decode_lm_m057_am_m0001/decode_lm_m057_am_m0001_analysis1_char/scoring_kaldi/test_filt.txt"
    filename_right = "/nas/material/users/berquist/expts/m0004/16k_som_exp/run_ensemble_tdnnf_15_backup/train_e2e/decode_analysis1_char/scoring/test_filt.txt"

    counts_left = make_counts(filename_left)
    counts_right = make_counts(filename_right)

    word_diff_in_left = counts_left - counts_right
    word_diff_in_right = counts_right - counts_left
    total_word_diff = word_diff_in_left | word_diff_in_right
    print(f"words only in left: {word_diff_in_left}")
    print(f"words only in right: {word_diff_in_right}")
    print(f"total counts of different words: {total_word_diff}")
