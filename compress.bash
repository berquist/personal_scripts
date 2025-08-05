#!/usr/bin/env bash

# Compress a directory or file to `.tar.gz` using a parallel compressor with
# the best compression.

filename="${1}"

TAR=tar
if command -v gtar 1>/dev/null 2>&1; then
    TAR=gtar
fi

${TAR} cf "${filename}".tar "${filename}"
pigz --best "${filename}".tar
