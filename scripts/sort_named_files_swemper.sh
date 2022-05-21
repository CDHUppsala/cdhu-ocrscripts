#!/bin/bash
# Author: ML/Authorfunction
# moves files into subfolders (that will be created) based on information in filename 
# copy this script, edit and run it in the directory where you keep files
# 
# Example command output from script:
# mkdir -p 1990
# mv Diabetes_1990_vol000_nr006.pdf 1990/Diabetes_1990_vol000_nr006.pdf

# turn on verbose to get feedback:
#set -x
FILE_PATTERN="*.pdf *.jpg *.txt"
SEPARATOR=_

shopt -s nullglob
for i in $FILE_PATTERN
do 
	INPUT_FILE=$i
	#edit and set separator
	#edit awk fields ($1,$2,$3 etc) depending on structure of filename
	#sed command at the end cleans up cases that end up with extra separators if fewer fields than standard:
	EXTENSION=${INPUT_FILE=##*.}
	DESTINATION=$(echo $INPUT_FILE | awk '{print $0}' | awk -F "${SEPARATOR}" -v sep="$SEPARATOR" '{print $2"/"$1sep$2sep$3sep$4sep$5}' | sed "s/$EXTENSION.*/$EXTENSION/") 
	SUB_FOLDER_STRING=$(echo $INPUT_FILE | awk '{print $0}' | awk -F "${SEPARATOR}" '{print $2}')
	# This is a hack to fix a edge case where extension sometimes get included in folder name:
	#SUB_FOLDER=$(echo $SUB_FOLDER | awk -F "\." '{print $1}')
	SUB_FOLDER=$(echo "${SUB_FOLDER_STRING%.*}")

	if [ "$1" == "-p" ]
	then
		#Uncomment this to run hot:
		mkdir -p $SUB_FOLDER
		mv $INPUT_FILE $DESTINATION
		: #nullcode so parsing continues if comment only (empty) block
		#echo Uncomment hot code for production run!
	else
		#echo commands for dry-run testing:
		echo mkdir -p $SUB_FOLDER
		echo mv $INPUT_FILE $DESTINATION
	fi
done
shopt -u nullglob

[ "$1" != "-p" ] && echo "Defaults to dry-run. Supply -p argument for production."
set +x