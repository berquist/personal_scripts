#!/usr/bin/env bash

filename="${1}"
tar cf "${filename}".tar "${filename}"
pigz --best "${filename}".tar
