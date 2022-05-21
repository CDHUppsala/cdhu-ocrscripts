#!/bin/zsh
# Author: ML/@authorfunction/CDHU
# copy/link this script, edit and run it in the directory where you keep image files that you want to ocr
# multi/thread/core version of ocr script, requires gnu parallel.
# ---------------------------
# If dealing with very large amounts of files, take note on this and adjust accordingly: https://stackoverflow.com/questions/47958163/tesseract-ocr-large-number-of-files
#
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
DO_DRY="--dry-run"
DO_SUPPRESS="2>/dev/null"
DO_LOG=""
CAFFEINATE=""
JOBS=6 #default to 6 threads/jobs, good for M1. Use option -j <jobs> to increase.
export OMP_THREAD_LIMIT=1 #run single thread per job,  https://github.com/tesseract-ocr/tesseract/issues/3109

echo $CDHU
# Check if mac os; if true use caffeinate:
[[ "$(uname)" == "Darwin" ]] && CAFFEINATE=caffeinate && echo "//Mac OS detected, will run with caffeinate to avoid sleep."

while getopts ":pvj:l:" option; do
	case $option in
		p) # check/set production run by clearing DO_DRY
        	DO_DRY="";;
		v) # check/set verbose by clearing DO_SUPPRESS
        	DO_SUPPRESS="";;
		j) JOBS=${OPTARG} ;; #echo "j is ${OPTARG}";;
		l) #LOGNAME=${OPTARG}# setup log
			DO_LOG="2>&1 | tee ocr.log";;
	esac
done

# SYNTAX GNU PARALLEL: parallel -j 8 convert {} -resize ... {} ::: *.png
# after ::: is file list/regex. {.} means basefilename w/o extension
$CAFFEINATE time parallel $DO_DRY --bar -j $JOBS '(tesseract -l '$OCR_LANG' "{}" "{.}" '$DO_SUPPRESS')' ::: *.$IMG_FORMAT 2>&1 | tee ocr.log
# Hacked this example to suppress stderr and keep progress bar: '(ffmpegthumbnailer -i "{}" -o "/tmp/${DIR}/{}.jpg" -f 2>/dev/null)'  ::: *.mp4

[ $DO_DRY ] && echo "Defaults to dry-run. Supply -p argument for production."
set +x