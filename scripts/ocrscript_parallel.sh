#!/bin/zsh
# Author: ML/Authorfunction
# copy this script, edit and run it in the directory where you keep image files that you want to ocr
# multicore version, requires gnu parallel
# requires tesseract-ocr and imagemagick (for image file conversions)
CDHU="\
 ____ ____ ____ ____ ________ 
||C |||D |||H |||U |||       
||__|||__|||__|||__|||_______
|/__\|/__\|/__\|/__\|/_______

 OCR TESSERACT / GNU PARALLEL
"

# turn on verbose to get feedback:
set -x
IMG_FORMAT=jpg
OCR_LANG=swe
DRY_ECHO=echo
CAFFEINATE=""
JOBS=6 #default to 6 threads/jobs, good for M1. Use option -j <jobs> to increase.

echo $CDHU
# Check if production run:
#[ "$1" != "-p" ] && DRY_ECHO=echo
# Check if mac os; if true use caffeinate:
[[ "$(uname)" == "Darwin" ]] && CAFFEINATE=caffeinate ; echo "On Mac OS, will run with caffeinate to avoid sleep"

while getopts ":pj:" option; do
   case $option in
      p) # set production run by clearing DRY_ECHO
         DRY_ECHO="";;
	  j) JOBS=${OPTARG} #echo "j is ${OPTARG}";;
   esac
done

find . -type f -name "*.jpg" \
	| sed "s/\.jpg//" \
	| $CAFFEINATE time \
	parallel --bar -j $JOBS $DRY_ECHO tesseract -l $OCR_LANG {}.jpg {} #> /dev/null 2>&1

[ "$1" != "-p" ] && echo "Defaults to dry-run. Supply -p argument for production."
set +x