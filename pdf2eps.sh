#!/bin/sh
# $Id: pdf2eps,v 0.01 2005/10/28 00:55:46 Herbert Voss Exp $
# Convert PDF to encapsulated PostScript.
# usage:
# pdf2eps <page number> <pdf file without ext> -> removed page number

pdfcrop "${1}.pdf" "${1}-temp.pdf"
pdftops -eps "${1}-temp.pdf" "${1}.eps"
rm "${1}-temp.pdf"

# pdfcrop "$2.pdf" "$2-temp.pdf"
# pdftops -f $1 -l $1 -eps "$2-temp.pdf" "$2.eps"
# rm "$2-temp.pdf"

#!/bin/sh
# $Id: pdf2eps,v 0.01 2005/10/28 00:55:46 Herbert Voss Exp $
# Convert PDF to encapsulated PostScript.
# usage:
# pdf2eps <page number> <pdf file without ext>

# pdfcrop $2.pdf
# pdftops -f $1 -l $1 -eps "$2-crop.pdf" 
# rm "$2-crop.pdf"
# mv "$2-crop.eps" $2.eps

# gs -q -dNOCACHE -dNOPAUSE -dBATCH -dSAFER -sDEVICE=epswrite -sOutputFile=${1}.eps ${1}.pdf
