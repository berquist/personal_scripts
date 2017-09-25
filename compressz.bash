#!/bin/bash

filename="${1}"
nproc="${2:$(nproc)}"
tar cf "${filename}"{.tar,}
zstd --rm -19 -T"${nproc}" "${filename}".tar
