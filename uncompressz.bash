#!/usr/bin/env bash

# Uncompress a `.tar.zst` archive.

basename="${1}"
unzstd "${basename}".tar.zst
tar xf "${basename}".tar
rm "${basename}".tar
