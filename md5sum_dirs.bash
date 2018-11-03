#!/usr/bin/env bash

hashfunc=md5sum

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
directories=$(printf "%s\n" "$@" | "$SCRIPTDIR"/basename_sort.pl)
echo "$directories"

for d in $directories; do
    hash=$(find "$d" -type f -not -path '*/\.git/*' -exec $hashfunc {} \; | sort -k 2 | $hashfunc)
    printf "%s %s\n" "$(echo "$hash" | cut -d ' ' -f 1)" "$d"
done
