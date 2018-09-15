#!/usr/bin/env bash

dir=${1:-${PWD}}

echo $(ls ${dir}/*.in | wc -w)
echo $(ls ${dir}/*.out | wc -w)
