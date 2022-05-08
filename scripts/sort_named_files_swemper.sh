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
FILE_EXT=pdf
SEPARATOR=_

for i in *.$FILE_EXT
do 
	INPUT_FILE=$i
	#edit and set separator
	#edit awk fields ($1,$2,$3 etc) depending on structure of filename:
	DESTINATION=$(echo $INPUT_FILE | awk '{print $0}' | awk -F "${SEPARATOR}" -v sep="$SEPARATOR" '{print $2"/"$1sep$2sep$3sep$4$5}')
	SUB_FOLDER=$(echo $INPUT_FILE | awk '{print $0}' | awk -F "${SEPARATOR}" '{print $2}')

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

[ "$1" != "-p" ] && echo "Defaults to dry-run. Supply -p argument for production."
set +x