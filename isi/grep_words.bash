#!/usr/bin/env bash

words="$@"

for word in ${words[@]}; do
    echo "${word}"
    rg -l "\b${word}\b" "${PWD}" | sort > "${PWD}/${word}.log"
done
