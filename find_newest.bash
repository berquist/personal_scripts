#!/bin/bash

# How to recursively find and list the latest modified files in a
# directory with subdirectories and times?

# https://stackoverflow.com/q/5566310/3249688

find "$1" -type f -print0 | xargs -0 stat --format '%Y :%y %n' | sort -nr | cut -d: -f2-

# without calling stat:
# find "$1" -type f -printf "%T@ %p\n"| sort -nr

# Mac:
# find "$1" -type f -exec stat -f "%m %N" "{}" \; | sort -nr
