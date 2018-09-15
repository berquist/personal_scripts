#!/usr/bin/env bash

# run_pdftotext.bash: Run `pdftotext` on all possible PDF files in the
# current working directory.

for f in $(find . -type f -name "*.pdf"); do
    stub="${f%.*}"
    echo "${f}"
    pdftotext -eol unix "${f}" > "${stub}".txt
done
