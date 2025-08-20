#!/usr/bin/env bash

while read pkg; do
    mapfile -t files < <(pacman -Qlq $pkg | grep -v /$)
    grep -Fq libgfortran.so.3 "${files[@]}" <&- 2> /dev/null && echo $pkg
done < <(pacman -Qqm)
