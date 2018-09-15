#!/usr/bin/env bash

for i in `iconv -l`
do
    echo "$i"
    iconv -f "$i" -t UTF-8 "$1" | grep "hint to tell converted success or not"
done &> /tmp/converted
