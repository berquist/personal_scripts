#!/usr/bin/env bash

# Which pages in the given PDF are in color?

# https://superuser.com/questions/234408/count-bw-color-pages-in-pdf#comment1874045_721773

file="$1"

gs -o - -sDEVICE=inkcov "$file" | tail -n +4 | sed '/^Page*/N;s/\n//' | sed -E '/Page [0-9]* 0.00000  0.00000  0.00000/d'
