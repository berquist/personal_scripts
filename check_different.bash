#!/usr/bin/env bash

comm -3 <(ls $1) <(ls $2)
