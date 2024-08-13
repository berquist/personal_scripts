#!/bin/sh

mkdir -p stashes
IFS='
'
for entry in $(git stash list); do
    stash_index=$(echo "${entry}" | sed -E "s/^stash@\{([[:digit:]]+)\}.*/\1/")
    filename="stashes/stash${stash_index}.diff"
    if [ -f "${filename}" ]; then
        echo "${filename} already exists, not overwriting"
    else
        git stash show --patch "stash@{${stash_index}}" > "${filename}"
    fi
done
