#!/usr/bin/env python3
# Author: ML/Authorfunction
# Script parses "Swemper-formatted" filename, like this example:
# Diabetes_1953_vol003_nr006.pdf
import sys
import os
import hashlib


DEBUG = False

def log(s):
    if DEBUG:
        print(s)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: scriptname.py swemperfilename")
        sys.exit()

    #works woth both existing and non-existing files supplied as argument
    swemper_file=os.path.basename(sys.argv[1])
    #remove extension
    filename=swemper_file.split(".")
    log(filename)
    volume_fields=filename[0].split("_")
    log(volume_fields)

    # Turn to dict
    #
    swemper_data = {
    "SwemperSeriesID": volume_fields[0],
    "FullPeriodicalName":"",
    "PeriodicalVolIdx":"",
    "PeriodicalNrIdx":"",
    "YearPublished": volume_fields[1]
    }
    log(swemper_data)

    #rebuild basefilename for md5 calc
    basefilename = volume_fields[0]+"_"+volume_fields[1]
    
    # get volume number if present
    for field in volume_fields:
        if "vol" in field:
            vol = field[3:] # slice to get number
            log(vol)
            swemper_data["PeriodicalVolIdx"] = vol
            basefilename = basefilename+"_"+field
    # get number if present
    for field in volume_fields:
        if "nr" in field:
            nr = field[2:] # slice to get number
            log(nr)
            swemper_data["PeriodicalNrIdx"] = nr
            basefilename = basefilename+"_"+field

    log(swemper_data)
    log(swemper_file)
    #calc md5 from filename.pdf and use as unique swemper-vol-id
    log(basefilename)
    md5 = hashlib.md5(basefilename.encode('utf-8')).hexdigest()

    # Format and print YAML
    #
    yaml_file=basefilename+".yaml"
    log(yaml_file)
    yaml_data = f"""\
%YAML 1.2
---
Swemper-yaml-filename: {yaml_file}
Swemper-volume-descriptor:
  SwemperSeriesID: &ssid {swemper_data["SwemperSeriesID"]}
  FullPeriodicalName: !!str {swemper_data["FullPeriodicalName"]}
  PeriodicalVolIdx: &vol !!str {swemper_data["PeriodicalVolIdx"]}
  PeriodicalNrIdx: &nr !!str {swemper_data["PeriodicalNrIdx"]}
  YearPublished: &yr {swemper_data["YearPublished"]}
  BaseFilename: 
    - *ssid
    - *yr
    - *vol
    - *nr
  Swemper-vol-id: {md5}
...
"""
print(yaml_data)