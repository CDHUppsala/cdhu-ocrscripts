#!/bin/zsh
# Author: ML/Authorfunction
# copy this script, edit and run it in the directory where you keep image files that you want to ocr
# requires tesseract-ocr and imagemagick (for image file conversions)

# turn on verbose to get feedback:
set -x
IMG_FORMAT=jpg #use png, jpg, tiff -- or pdf but see below for that
OCR_LANG=swe

#note: recursive glob **/* to find pdfs in subdors requires zsh shebang
#update: should also work in bash after setting "shopt -s globstar"
for i in **/*.$IMG_FORMAT
do 
	#*uncomment* these lines if you want to process single page pdfs:
	#convert -density 300 -compress lzw $i temp.tif
	#INPUT_FILE=temp.tif
	# ... and *comment* this line (for pdf processing):
	INPUT_FILE=$i
	# Bash pattern ${VAR%pattern} – removes file extension from filename:
	OUTPUT_BASENAME=${i%.*}
	tesseract -l $OCR_LANG $INPUT_FILE $OUTPUT_BASENAME

	# ...again, comment/uncomment depending on pdf or not
	#rm temp.tif
done
set +x
