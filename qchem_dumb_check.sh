#!/usr/bin/env sh

ls ./*.in | wc -w
ls ./*.out | wc -w
grep -L "Have a nice day" ./*.out
