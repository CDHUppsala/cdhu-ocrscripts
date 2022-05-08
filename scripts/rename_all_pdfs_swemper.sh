#!/bin/bash
# Author: ML/Authorfunction
# Copy this script, edit and run it in the directory with pdfs
# Requires: dflow2filename_swemper.py 

# turn on verbose to get feedback:
#set -x
#IMG_FORMAT=jpg #use png, jpg, tiff -- or pdf but see below for that
#OCR_LANG=swe
CSV_SOURCE="../periodika_diabetes_dflowID.csv"

for i in *.pdf
do 
	INPUT_FILE=$i
	# Bash pattern ${VAR%pattern} – removes file extension from filename:
	#OUTPUT_BASENAME=${i%.*}
	#tesseract -l $OCR_LANG $INPUT_FILE $OUTPUT_BASENAME
	NEW_FILENAME=$(./dflow2filename_swemper.py $CSV_SOURCE $INPUT_FILE)
	#use echo for dry run...
	#echo mv $INPUT_FILE $NEW_FILENAME
	#use cp for security
	cp $INPUT_FILE renamed/$NEW_FILENAME


done
set +x