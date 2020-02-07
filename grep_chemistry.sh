#!/bin/bash

find ~/data/Chemistry -type f -name "*.in" -print0 2>/dev/null 1>find.log
# sort find.log > find_sorted.log
# \rm find.log
# \mv find_sorted.log find.log
< find.log xargs -0 rg -F 'sapt2'
