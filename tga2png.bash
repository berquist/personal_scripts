#!/usr/bin/env bash

for image in *.tga
do
    filename=${image%.*}
    echo ${filename}
    convert ${filename}.tga ${filename}.png
done
