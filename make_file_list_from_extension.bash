#!/usr/bin/env bash

# Given a file extension, get the list of all files in the current working
# directory with their full paths.

set -euo pipefail

function make_file_list {
    extension=$1
    if [[ -z ${extension} ]]; then
        exit 1
    fi
    # shellcheck disable=SC2231
    for file in *.${extension}; do
        path="${PWD}/${file}"
        printf "%s\n" "${path}"
    done
}

make_file_list "$1" > list.txt
