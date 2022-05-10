#!/usr/bin/env python3
# Author: ML/Authorfunction
# This is python code called by shell scripts: rename_all_pdfs_swemper.sh
# Finds dflow-ids and get metadata from csv, which can be used to rename pdf-files properly.
# Script returns "Swemper-formatted" filename, like this example:
# Diabetes_1953_vol003_nr006.pdf
# Prior to use: convert dflow xslsx to csv with ssconv (in gnumeric package). Xslsx file is delivered by Library scanning procedure.
#
# CSV-file is formatted like this:
# Libris-ID,Titel,Årgång,Nr,År,dFlow-ID,Datum,Operatör,Kommentar
# 8262498,Diabetes,1,1,1949,121986,,,
# 8262498,Diabetes,1,2,1949,121987,,,
# ...
#

import sys
import os
import csv

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: scriptname.py csvfile.csv pdffile.pdf")
        sys.exit()

    pdf_file=os.path.basename(sys.argv[2])
    with open(sys.argv[1]) as csvfile:
        swemper_csv = csv.DictReader(csvfile, delimiter = ",")
        swemper_dict = list(swemper_csv)
        filename=pdf_file
        #remove extension
        filename=filename.split(".", 1)
        #print(filename)
        for row in swemper_dict:
            if row['dFlow-ID'] == filename[0]:
                    newfilename = ( 
                                row['Titel']+"_"
                                +row['År']
                                +"_vol"
                                +row['Årgång'].zfill(3)
                                +"_nr"
                                +row['Nr'].zfill(3)
                                +"."
                                +filename[1]
                    )
                    print(newfilename)