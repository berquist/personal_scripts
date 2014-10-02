#!/bin/bash

images=`ls *.tga`

for image in ${images}
do
    filename=${image%.*}
    echo ${filename}
    convert ${filename}.tga ${filename}.png
done
