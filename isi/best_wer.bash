#!/usr/bin/env bash

BEST_WER=/nas/material/users/jbilla/eesen/asr_egs/wsj/utils/best_wer.sh

# find . -type d -name "decode_analysis1*" 2>/dev/null
# run from mnnnn directory
(for i in 16k_kchar/tdnnf_char_chain/train_e2e/decode_analysis1_*; do
     grep WER $i/wer_* | ${BEST_WER};
 done) | sort -k2,2
