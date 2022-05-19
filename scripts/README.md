# Utility scripts for scanning post-processing/OCR/Swemper projects at CDHU

### burstpdf.sh
Utility to burst pdfs into single page image files using ImageMagick convert.

### extracttext.sh
Utility to extract previously ocr:d text from pdfs and output it as textfiles.

### dflow2filename_swemper.py
Script takes dFlow ID and metadata delivered through library scanning process (Gothenburg/Alvin) and outputs filename according to Swemper-specification/scheme to stdout. This python code is wrapped by rename_all_pdfs_swemper.sh.

### rename_all_pdfs_swemper.sh
Script wraps and runs dflow2filename_swemper.py to (recursively/zsh) rename all pdfs in a directory structure according to Swemper-specification/scheme.

### parse_swemper_filename.py
Script parses a file named according to the Swemper naming scheme and outputs Swemeper yaml data to stdout. This script is wrapped by generate_swemper_yaml.sh.

### generate_swemper_yaml.sh
Wraps parse_swemper_filename.py to generate Swemper yaml files recursively throughout a directory hierarchy.

### sort_named_files_swemper.sh
Script reads Swemper filenames in a directory, extracts publication year (with awk); creates subfolders for year and moves the files into them.

### ocrscript.sh
Script to apply Tesseract OCR pdfs or images in a directory structure (recursively/zsh).

### ocrscript_parallel.sh
Script parallelizes Tesseract OCR GNU Parallel.

## Swemper filename scheme and directory structure
//TODO convention and example

 Filename example 1: 1952/Diabetes_1952_vol002_nr001.pdf
 
 Filename example 2: 1952/Diabetes_1952_vol002_nr001_0031.jpg
 
 Naming convention is flexible...
 
     This is ok: 1918/Lakartidningen_1918_0112.jpg
 
     Also ok: Status_1955_vol015_nr12CJulen1955medglimtar.pdf
 
     Also ok: Status_1955_vol015_nr12CJulen1955medglimtar_0048.jpg

## Swemper YAML metadata physical volume descriptor
//TODO convention and example

```shell
Diabetes_1949-1990$ ./parse_swemper_filename.py 1952/Diabetes_1952_vol002_nr001.pdf
```

```yaml
%YAML 1.2
---
Swemper-yaml-filename: Diabetes_1952_vol002_nr001.yaml
Swemper-volume-descriptor:
  SwemperSeriesID: &ssid Diabetes
  FullPeriodicalName: !!str 
  PeriodicalVolIdx: &vol !!str 002
  PeriodicalNrIdx: &nr !!str 001
  YearPublished: &yr 1952
  BaseFilename: 
    - *ssid
    - *yr
    - *vol
    - *nr
  Swemper-vol-id: 4e1eca51f714326501b6452b7a81e54a
...
```

