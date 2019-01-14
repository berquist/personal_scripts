#!/usr/bin/env bash

## get the inner filenames from all nested zip files

(
    for zipfile in $(find . -type f -name "*.zip"); do
        unzip -l "${zipfile}" > zipfile_listing.tmp
        < zipfile_listing.tmp tail -n +4 | sed '$d' | sed '$d'
    done
) > zipfile_listing_cat.tmp
rm zipfile_listing.tmp
< zipfile_listing_cat.tmp awk '{ print $4 }' | sort -u
rm zipfile_listing_cat.tmp
