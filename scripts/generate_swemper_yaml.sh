#!/bin/zsh
# Author: ML/Authorfunction
# copy this script, edit and run it in the directory structure where yaml files are to be generated

# turn on verbose to get feedback:
#set -x
IMG_FORMAT=pdf # only look for pdfs as source of volume-data

#note: recursive glob **/* to find pdfs in subdors requires zsh shebang
for i in **/*.$IMG_FORMAT
do 
	INPUT_FILE=$i
	#edit and set separator
	#edit awk fields ($1,$2,$3 etc) depending on structure of filename:
	#DESTINATION=$(echo $INPUT_FILE | awk '{print $0}' | awk -F "${SEPARATOR}" -v sep="$SEPARATOR" '{print $2"/"$1sep$2sep$3sep$4$5}')
	#SUB_FOLDER=$(echo $INPUT_FILE | awk '{print $0}' | awk -F "${SEPARATOR}" '{print $2}')
	# Bash pattern ${VAR%pattern} – removes file extension from filename:
	OUTPUT_BASENAME=${i%.*}

	if [[ "$1" == "-p" ]]
	then
		#Uncomment this to run hot:
		echo $OUTPUT_BASENAME.yaml
		./parse_swemper_filename.py $i > $OUTPUT_BASENAME.yaml
		: #nullcode so parsing continues if comment only (empty) block
		#echo Uncomment hot code for production run!
	else
		#echo commands for dry-run testing:
		echo "./parse_swemper_filename.py $i > $OUTPUT_BASENAME.yaml"
	fi
done

[ "$1" != "-p" ] && echo "Defaults to dry-run. Supply -p argument for production."
set +x