#!/bin/bash

filename="${1}"
unzstd "${filename}".tar.zst
tar xf "${filename}".tar
rm "${filename}".tar
