#!/usr/bin/env bash

# [berquist@vista-dev01 /nas/material/users/berquist/expts/m0001/16k_kchar/tdnnf_char_chain]$ ~/personal_scripts/isi/best_wer.bash ls
# ---
# This is the best baseline model.
# %WER 57.07 [ 51740 / 90655, 5528 ins, 16704 del, 29508 sub ] train_e2e/decode_analysis1_char_exp_fg/wer_10_0.0
# ---
# %WER 57.37 [ 52010 / 90655, 6268 ins, 13936 del, 31806 sub ] train_e2e/decode_analysis1_char_exp_4gcarpa/wer_9_0.0
# %WER 57.95 [ 52537 / 90655, 5519 ins, 16905 del, 30113 sub ] train_e2e/decode_analysis1_char_exp/wer_10_0.0
# %WER 58.19 [ 52754 / 90655, 5234 ins, 17083 del, 30437 sub ] train_e2e/decode_analysis1_char_exp_3gcarpa/wer_10_0.0
# %WER 68.45 [ 62054 / 90655, 5989 ins, 19206 del, 36859 sub ] train_e2e/decode_analysis1_char_3gcarpa/wer_9_1.0
# %WER 68.74 [ 62316 / 90655, 6116 ins, 20014 del, 36186 sub ] train_e2e/decode_analysis1_char_tg/wer_9_1.0
# %WER 68.97 [ 62526 / 90655, 5380 ins, 21742 del, 35404 sub ] train_e2e/decode_analysis1_char_4gcarpa/wer_10_0.5
# %WER 69.21 [ 62738 / 90655, 5082 ins, 21075 del, 36581 sub ] train_e2e/decode_analysis1_char_elex_fg/wer_10_0.0
# %WER 69.30 [ 62820 / 90655, 4927 ins, 24613 del, 33280 sub ] train_e2e/decode_analysis1_char/wer_10_0.5
# %WER 69.67 [ 63163 / 90655, 4918 ins, 20890 del, 37355 sub ] train_e2e/decode_analysis1_char_elex_3gcarpa/wer_10_0.0
# %WER 70.27 [ 63700 / 90655, 4833 ins, 22103 del, 36764 sub ] train_e2e/decode_analysis1_char_elex/wer_10_0.0
# %WER 70.72 [ 64111 / 90655, 4749 ins, 21089 del, 38273 sub ] train_e2e/decode_analysis1_char_elex_4gcarpa/wer_10_0.0
# The strange discrepancy is because the analysis1 decode isn't done yet.
# [berquist@vista-dev01 /nas/material/users/berquist/expts/m0003/16k_char/tdnnf_char_chain]$ ~/personal_scripts/isi/best_wer.bash
# %WER 57.37 [ 52010 / 90655, 6268 ins, 13936 del, 31806 sub ] train_e2e/decode_analysis1_char_exp_4gcarpa/wer_9_0.0
# %WER 57.95 [ 52532 / 90655, 5520 ins, 16945 del, 30067 sub ] train_e2e/decode_analysis1_char_exp/wer_10_0.0
# %WER 58.19 [ 52754 / 90655, 5234 ins, 17083 del, 30437 sub ] train_e2e/decode_analysis1_char_exp_3gcarpa/wer_10_0.0
# %WER 59.12 [ 53593 / 90655, 6134 ins, 15438 del, 32021 sub ] train_e2e/decode_analysis1_char_exp_fg/wer_10_0.0
# %WER 68.91 [ 62472 / 90655, 5906 ins, 20719 del, 35847 sub ] train_e2e/decode_analysis1_char_tg/wer_9_1.0
# %WER 69.34 [ 62859 / 90655, 5608 ins, 21118 del, 36133 sub ] train_e2e/decode_analysis1_char/wer_9_1.0
# %WER 69.74 [ 63226 / 90655, 6621 ins, 18139 del, 38466 sub ] train_e2e/decode_analysis1_char_3gcarpa/wer_9_1.0
# %WER 70.29 [ 63719 / 90655, 4824 ins, 22161 del, 36734 sub ] train_e2e/decode_analysis1_char_elex/wer_10_0.0
# %WER 70.51 [ 63924 / 90655, 6456 ins, 18218 del, 39250 sub ] train_e2e/decode_analysis1_char_4gcarpa/wer_9_1.0
# %WER 70.97 [ 64336 / 90655, 4294 ins, 22192 del, 37850 sub ] train_e2e/decode_analysis1_char_elex_fg/wer_9_1.0
# %WER 71.61 [ 64918 / 90655, 5482 ins, 18640 del, 40796 sub ] train_e2e/decode_analysis1_char_elex_3gcarpa/wer_9_0.5
# %WER 71.94 [ 65214 / 90655, 4557 ins, 19070 del, 41587 sub ] train_e2e/decode_analysis1_char_elex_4gcarpa/wer_8_1.0

# Hmmm?
# %WER 57.95 [ 52532 / 90655, 5520 ins, 16945 del, 30067 sub ] train_e2e/decode_analysis1_char_exp/wer_10_0.0
# %WER 59.10 [ 53581 / 90655, 5649 ins, 16039 del, 31893 sub ] train_e2e/decode_analysis1_char_exp_4gcarpa/wer_10_0.0
# %WER 59.12 [ 53593 / 90655, 6134 ins, 15438 del, 32021 sub ] train_e2e/decode_analysis1_char_exp_fg/wer_10_0.0
# %WER 60.23 [ 54603 / 90655, 5536 ins, 15630 del, 33437 sub ] train_e2e/decode_analysis1_char_exp_3gcarpa/wer_9_0.5
# %WER 68.91 [ 62472 / 90655, 5906 ins, 20719 del, 35847 sub ] train_e2e/decode_analysis1_char_tg/wer_9_1.0
# %WER 69.34 [ 62859 / 90655, 5608 ins, 21118 del, 36133 sub ] train_e2e/decode_analysis1_char/wer_9_1.0
# %WER 69.74 [ 63226 / 90655, 6621 ins, 18139 del, 38466 sub ] train_e2e/decode_analysis1_char_3gcarpa/wer_9_1.0
# %WER 70.29 [ 63719 / 90655, 4824 ins, 22161 del, 36734 sub ] train_e2e/decode_analysis1_char_elex/wer_10_0.0
# %WER 70.51 [ 63924 / 90655, 6456 ins, 18218 del, 39250 sub ] train_e2e/decode_analysis1_char_4gcarpa/wer_9_1.0
# %WER 70.97 [ 64336 / 90655, 4294 ins, 22192 del, 37850 sub ] train_e2e/decode_analysis1_char_elex_fg/wer_9_1.0
# %WER 71.61 [ 64918 / 90655, 5482 ins, 18640 del, 40796 sub ] train_e2e/decode_analysis1_char_elex_3gcarpa/wer_9_0.5
# %WER 72.71 [ 65916 / 90655, 5520 ins, 19347 del, 41049 sub ] train_e2e/decode_analysis1_char_elex_4gcarpa/wer_10_0.0


BEST_WER=/nas/material/users/jbilla/eesen/asr_egs/wsj/utils/best_wer.sh
ROOT_DIR=/nas/material/users/berquist/expts/m0003

# for i in 
