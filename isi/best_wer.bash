#!/usr/bin/env bash

BEST_WER=/nas/home/berquist/opt/apps/build/kaldi/egs/wsj/s5/utils/best_wer.sh

# find . -type d -name "decode_analysis1*" 2>/dev/null
(for i in decode*analysis1*; do
     grep WER $i/wer_* | ${BEST_WER};
 done) | sort -k2,2
