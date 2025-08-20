#!/usr/bin/env bash

# An example of looking for files, saving the results as an intermediate, then
# grepping through each.

fd -t f -F -e in -0 . ~/data/Chemistry 2> /dev/null 1> find.log
# sort find.log > find_sorted.log
# \rm find.log
# \mv find_sorted.log find.log
< find.log xargs -0 rg -F 'sapt2'
