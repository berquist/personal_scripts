#!/bin/bash

for pdf in $(find * -maxdepth 0 -name "*.pdf"); do pdf2eps.sh ${pdf//%.*}; done
