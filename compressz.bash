#!/usr/bin/env bash

# Compress a directory or file to `.tar.zst` with the best compression.

basename="${1}"
nproc="${2:$(nproc)}"
tar cf "${basename}"{.tar,}
zstd --rm -19 -T"${nproc}" "${basename}".tar
