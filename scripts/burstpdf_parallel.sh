#!/bin/zsh
# Author: ML/@authorfunction/CDHU
# copy/link this script, edit and run it in the directory where you keep image files that you want to ocr
# multi/thread/core version of ocr script, requires gnu parallel.
CDHU="\
 ____ ____ ____ ____ ________ 
||C |||D |||H |||U |||       
||__|||__|||__|||__|||_______
|/__\|/__\|/__\|/__\|/_______

//IMAGEMAGICK////GNU PARALLEL
"

# turn on verbose to get feedback:
#set -x
IMG_FORMAT=jpg
OCR_LANG=swe
DO_DRY="--dry-run"
DO_SUPPRESS="2>/dev/null"
CAFFEINATE=""
JOBS=6 #default to 6 threads/jobs, good for M1. Use option -j <jobs> to increase.
export OMP_THREAD_LIMIT=1 #run single thread per job,  https://github.com/tesseract-ocr/tesseract/issues/3109
QUALITY=90
DENSITY=300
DO_REMOTE=""
#DO_REMOTE="-Smatts@beast --transfer --return {.*} --cleanup"

echo $CDHU
# Check if mac os; if true use caffeinate:
[[ "$(uname)" == "Darwin" ]] && CAFFEINATE=caffeinate && echo "//Mac OS detected, will run with caffeinate to avoid sleep."

while getopts ":pvj:" option; do
	case $option in
		p) # check/set production run by clearing DO_DRY
        	DO_DRY="";;
		v) # check/set verbose by clearing DO_SUPPRESS
        	DO_SUPPRESS="";;
		j) JOBS=${OPTARG} #echo "j is ${OPTARG}";;
	esac
done

# SYNTAX GNU PARALLEL: parallel -j 8 convert {} -resize ... {} ::: *.png
# after ::: is file list/regex. {.} means basefilename w/o extension
#$CAFFEINATE time parallel $DO_DRY --bar -j $JOBS '(tesseract -l '$OCR_LANG' "{}" "{.}" '$DO_SUPPRESS')' ::: *.$IMG_FORMAT
# Hacked this example to suppress stderr and keep progress bar: '(ffmpegthumbnailer -i "{}" -o "/tmp/${DIR}/{}.jpg" -f 2>/dev/null)'  ::: *.mp4
$CAFFEINATE time parallel $DO_DRY --bar -j $JOBS $DO_REMOTE '(convert -density '$DENSITY' "{}" -quality '$QUALITY' "{.}"_%04d.'$IMG_FORMAT' '$DO_SUPPRESS')' ::: *.pdf

[ $DO_DRY ] && echo "Defaults to dry-run. Supply -p argument for production."
set +x