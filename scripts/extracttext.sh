#!/bin/bash
# Author: ML/Authorfunction
# Extracts text (already ocr:d) from pdfs.
# copy this script, edit and run it in the directory where you keep pdf files with text to extract
# requires pdftotext (on mac use brew install xpdf to install)

# turn on verbose to get feedback:
set -x

for i in *.pdf
do 
	INPUT_FILE=$i
	# Bash pattern ${VAR%pattern} – removes file extension from filename:
	OUTPUT_BASENAME=${i%.*}
	#  pdftotext -enc UTF-8 121986.pdf out.txt
	pdftotext -enc UTF-8 $INPUT_FILE $OUTPUT_BASENAME.txt
done
set +x