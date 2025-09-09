#!/bin/sh

# findclass.sh: https://stackoverflow.com/a/68411760

unzip -l "$1" 2> /dev/null | grep $2 > /dev/null 2>&1 && echo "$1"
