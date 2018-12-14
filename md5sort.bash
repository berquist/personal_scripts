#!/usr/bin/env bash

# files=$(find "${1}" -type f -print0)
# xargs -0

md5s=$(find "${1}" -type f -print0 | xargs -0 md5)
echo "${md5s}" > md5s.log
md5s_sorted=$(awk '{ print $NF, $0 }' md5s.log | sort -n -k1)
echo "${md5s_sorted}" > md5s_sorted.log
md5s_trimmed=$(< md5s_sorted.log grep -v "flac" | grep -v "m4a" | grep -v "mp3" | grep -v "DS_Store" | grep -v "Thumbs.db" | grep -v "txt")
echo "${md5s_trimmed}" > md5s_trimmed.log
