#!/bin/zsh
# Author: ML/Authorfunction
# Copy this script, edit and run it in the directory with pdfs
# Requires: dflow2filename_swemper.py 

# turn on verbose to get feedback:
#set -x
CSV_SOURCE="./periodika_status_dflowID.csv"
c=0

for i in **/*.pdf
do 
	INPUT_FILE=$i
	let "c++"
	# Bash pattern ${VAR%pattern} – removes file extension from filename:
	#OUTPUT_BASENAME=${i%.*}
	NEW_FILENAME=$(./dflow2filename_swemper.py $CSV_SOURCE $INPUT_FILE)

	if [[ "$1" == "-p" ]]
	then
		#Uncomment this to run hot:
		: #nullcode so parsing continues if comment only (empty) block
		#echo Uncomment hot code for production run!
		#use cp for security
		echo cp $INPUT_FILE renamed/$NEW_FILENAME
	else
		#echo commands for dry-run testing:
		echo mv $INPUT_FILE $NEW_FILENAME	
	fi

done

[ "$1" != "-p" ] && echo "Dry-run complete: Will rename/move $c files." || echo "Production run complete: Renamed/moved $c files."
[ "$1" != "-p" ] && echo "Defaults to dry-run. Supply -p argument for production."
set +x