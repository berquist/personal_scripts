#!/usr/bin/env sh

emacs --batch -l ert -l "${1}" -f ert-run-tests-batch-and-exit
