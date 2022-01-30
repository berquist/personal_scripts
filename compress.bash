#!/usr/bin/env bash

# Compress a directory or file to `.tar.gz` using a parallel compressor with
# the best compression.

filename="${1}"
tar cf "${filename}".tar "${filename}"
pigz --best "${filename}".tar
