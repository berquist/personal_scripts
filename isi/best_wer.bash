#!/usr/bin/env bash

BEST_WER=/nas/home/berquist/opt/apps/build/kaldi/egs/wsj/s5/utils/best_wer.sh

(for i in decode*analysis*; do
     grep WER $i/wer_* | ${BEST_WER};
 done) | sort -k2,2
