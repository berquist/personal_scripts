#!/usr/bin/env bash

hashfunc=md5sum

directories=$(printf "%s\n" "$@" | ./basename_sort.pl)
echo "$directories"

for d in $directories; do
    hash=$(find "$d" -type f -not -path '*/\.git/*' -exec $hashfunc {} \; | sort -k 2 | $hashfunc)
    printf "%s %s\n" "$hash" "$d"
done
