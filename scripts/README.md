# Utility scripts for scanning post-processing/OCR/Swemper projects at CDHU

## burstpdf.sh
Utility to burst pdfs into single page image files using ImagMagick convert.

## extracttext.sh
Utility to extract previously ocr:d text from pdfs and output it as textfiles.

## dflow2filename_swemper.py
Script takes dFlow ID and metdata delivered through library scanning process (Gothenburg/Alvin) and outputs filename according to Swemper-specification/scheme to stdout. This python code is wrapped by rename_all_pdfs_swemper.sh.

## rename_all_pdfs_swemper.sh
Script wraps and runs dflow2filename_swemper.py to (recursively/zsh) rename all pdfs in a directory structure ackording to Swemper-specification/scheme.

## parse_swemper_filename.py
Script parses a file named according to the Swemper naming scheme and outputs Swemeper yaml data to stdout. This script is wrapped by generate_swemper_yaml.sh.

## generate_swemper_yaml.sh
Wraps parse_swemper_filename.py to generate Swemper yaml files recursively throughout a directory hierarchy.

## sort_named_files_swemper.sh
Script reads Swemper filenames in a directory, extracts publication year (with awk); creates subfolders for year and moves the files into them.

## ocrscript.sh
Script to apply tesseract ocr to pdfs or images in a directory structure (recursively/zsh).
