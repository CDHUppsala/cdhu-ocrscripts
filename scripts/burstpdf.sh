#!/bin/bash
# copy this script, edit and run it in the directory where you keep pdf files to convert to images
# requires imagemagick

# turns on verbose to get feedback:
set -x
IMG_FORMAT=jpg #use png, jpg, tiff etc. Not sure if -quality option applies to anything but jpg though.
DENSITY=300
QUALITY=90
OCR_LANG=swe

for i in *.pdf
do 
	INPUT_FILE=$i
	# Bash pattern ${VAR%pattern} – removes file extension from filename:
	OUTPUT_BASENAME=${i%.*}
	# %04d ==> "0001.jpg" etc
	convert -density $DENSITY $INPUT_FILE -quality $QUALITY ${OUTPUT_BASENAME}_%04d.$IMG_FORMAT
done
set +x
