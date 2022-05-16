#!/bin/zsh
# Author: ML/Authorfunction
# copy this script, edit and run it in the directory where you keep image files that you want to ocr
# multi/thread/core version of ocr script, requires gnu parallel
CDHU="\
 ____ ____ ____ ____ ________ 
||C |||D |||H |||U |||       
||__|||__|||__|||__|||_______
|/__\|/__\|/__\|/__\|/_______

 OCR TESSERACT / GNU PARALLEL
"

# turn on verbose to get feedback:
#set -x
IMG_FORMAT=jpg
OCR_LANG=swe
DRY_ECHO="--dry-run"
CAFFEINATE=""
JOBS=6 #default to 6 threads/jobs, good for M1. Use option -j <jobs> to increase.
export OMP_THREAD_LIMIT=1 #run single thread per job,  https://github.com/tesseract-ocr/tesseract/issues/3109

echo $CDHU
# Check if mac os; if true use caffeinate:
[[ "$(uname)" == "Darwin" ]] && CAFFEINATE=caffeinate ; echo "On Mac OS, will run with caffeinate to avoid sleep"

while getopts ":pj:" option; do
	case $option in
		p) # check/set production run by clearing DRY_ECHO
        	DRY_ECHO="";;
		j) JOBS=${OPTARG} #echo "j is ${OPTARG}";;
	esac
done

# SYNTAX GNU PARALLEL: parallel -j 8 convert {} -resize ... {} ::: *.png
# after ::: is file list/regex. {.} means basefilename w/o extension
$CAFFEINATE time parallel $DRY_ECHO --bar -j $JOBS '(tesseract -l '$OCR_LANG' "{}" "{.}" 2>/dev/null)' ::: *.$IMG_FORMAT
# Hacked this example to suppress stderr and keep progress bar: '(ffmpegthumbnailer -i "{}" -o "/tmp/${DIR}/{}.jpg" -f 2>/dev/null)'  ::: *.mp4

[ $DRY_ECHO ] && echo "Defaults to dry-run. Supply -p argument for production."
set +x