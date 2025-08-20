#!/bin/bash

# Taken from https://wiki.math.cmu.edu/iki/wiki/tips/20140301-git-latexdiff.html

# Make sure inputs are tex files
LOCAL="$1"
REMOTE="$2"
MERGED="$3"

if [[ "${MERGED##*.}" == tex ]]; then
    output="${MERGED%.tex}-diff.tex"

    # if [[ -f "$output" ]]; then
    #     read -p "File $output exists. Overwrite? " confirm
    #     [[ "$confirm" != y && "$confirm" != yes ]] && exit 1
    # fi

    latexdiff -t CFONT "$LOCAL" "$REMOTE" > "$output"
    echo "Generated $output"
else
    echo "Skipped $MERGED (non tex)."
fi
