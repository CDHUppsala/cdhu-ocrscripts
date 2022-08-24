#!/usr/bin/env python3
# Author: ML/Authorfunction
import hashlib
import sys
from datetime import date
import pyperclip as clipboard
import PySimpleGUI as sg
from ruamel.yaml import YAML

# GLOBAL NAMESPACE
DEBUG = True
WIDTH = 1000
HEIGHT = 800
basename = ""
yaml_basename = ""
yaml_data = ""
info_string = """ 
 ____ ____ ____ ____ ______________
||C |||D |||H |||U |||       
||__|||__|||__|||__|||_____________
|/__\|/__\|/__\|/__\|/_____________

SWEMPER TOOL 𝛼/ver / INSTRUCTIONS:
"""
info = '''
1) Fill in pre-flight fields. Copy filename and paste into scanner-software.
2) Operate the scanner.
3) Fill in post-flight fields.
'''

swemper_data = {}


def log(s):
    if DEBUG:
        # print('------------------')
        print(s)


def init_layout():
    sg.theme('DarkBlue2')
    try:
        sg.set_options(font=("Menlo", 16))
        #sg.set_options(font=("UbuntuMono Nerd Font", 17))
        #sg.set_options(font=("Inconsolata", 17))
        #sg.set_options(font=("Source Code Pro ExtraLight Regular", 16))
        # sg.set_options(font=("Fira Code", 16)) #/Users/mattslindstrom/Downloads/Monoid-HalfTight-Dollar-0/Monoid-Retina-HalfTight-Dollar-0.ttf
        #sg.set_options(font=("Monoid HalfTight Regular", 16))
    except:
        sg.set_options(font=("Courier", 16))
        print("//No fancy monospaced font available. Use Courier as fallback.")

    tab0 = [

        [  # row 0
            sg.Text("SwemperSeriesID:"),
            sg.Input(key='SwemperSeriesID',
                     default_text="Status", expand_x=True)
        ],  # row 1
        [
            sg.Text("FullPeriodicalName:"),
            sg.Input(key='FullPeriodicalName',
                     default_text="Status", expand_x=True)
        ],
        [
            sg.Text("PeriodicalVolIdx:"),
            sg.Input(key='PeriodicalVolIdx', expand_x=True)
        ],
        [
            sg.Text("PeriodicalNrIdx:"),
            sg.Input(key='PeriodicalNrIdx', expand_x=True)
        ],
        [   # ...final row
            sg.Text("YearPublished:"),
            sg.Input(key='YearPublished',
                     default_text="1958", expand_x=True)
        ],

    ]

    tab1 = [

        [  # row 0
            sg.Text("NumberOfScannedPages"),
            sg.Input(key='NumberOfScannedPages',
                     default_text="", expand_x=True)
        ],  # row 1
        [
            sg.Text("FinalPrintedPageNumber"),
            sg.Input(key='FinalPrintedPageNumber',
                     default_text="", expand_x=True)
        ],
        [
            sg.Text("DateOfScan"),
            sg.Input(key='DateOfScan',
                     default_text=date.today().isoformat(), expand_x=True)
        ],
        [
            sg.Text("Comment"),
            sg.Input(key='Comment', expand_x=True)
        ],
        [
            sg.Text("//WhateverIsUseful:"),
            sg.Input(key='Whatever',
                     default_text="", expand_x=True)
        ],
    ]

    col0 = [

        # TABS GO HERE
        [sg.TabGroup([[sg.Tab('PRE-FLIGHT', tab0, border_width=0, p=0), ],
                      [sg.Tab('POST-FLIGHT', tab1, border_width=0, p=0), ]],
                     border_width=0, tab_border_width=0, selected_background_color='White', selected_title_color='Black', p=0)],
        ###############
        [
            sg.Text("Base filename to copy:"),
            sg.Input(key='thebasename',
                     default_text="<Copy this>", expand_x=True)
        ],
        [  # BUTTON ROW
            sg.Button('UPDATE YAML', key='//UPDATE',
                      bind_return_key=True, p=((0, 0), (20, 10))),
            sg.Button('COPY F-NAME', key='//COPY', p=((10, 0), (20, 10))),
            sg.Button('WRITE YAML', key='//WRITE',
                      disabled=False, p=((10, 0), (20, 10))),
            sg.Button('EXIT', key='EXIT', p=((10, 0), (20, 10))),
        ],
        [  # ...last row
            sg.Multiline(size=(50, 80), expand_y=True,
                         key='textbox', expand_x=True, p=((0, 0), (0, 0)))
        ],
    ]

    # TEMPLATE FOR GUI COLUMN
    # colNN = [
    #     [sg.Text("row 1"), sg.Text("row 1"), sg.Text("row 1")],  # Row 0
    #     [sg.Text("row 2"), sg.Text("row 2"), sg.Text("row 2")],  # Row 1
    #     [sg.Text("row 3"), sg.Text("row 2"), sg.Text("row m")],  # Row m
    # ]

    col1 = [
        [sg.Text(info_string, p=0)],  # Row 0
        [sg.Text(info, p=0, size=(38, 20))],  # Row 1
        [sg.Multiline('-- stdout --\n', p=10, size=(38, 20),
                      reroute_stdout=True, autoscroll=True)],  # Row 2

    ]

    layout = [
        [
            sg.Column(col0, size=(WIDTH/2+(WIDTH/12), HEIGHT),
                      expand_x=True, expand_y=True, pad=(15, 10)),  # left col


            sg.Column(col1, justification='right', element_justification='left',
                      vertical_alignment='top', pad=0)  # right col
        ]
    ]
    return layout


def main():
    # Initialize and create GUI
    layout = init_layout()

    # yaml = YAML()
    # with open('default.yaml') as f:
    #     swemper_data = yaml.load(f)

    window = sg.Window('Swemper YAML Tool', layout,
                       size=(WIDTH, HEIGHT), resizable=True)

    # MAIN EVENT LOOP #
    while True:
        event, swemper_data = window.read()
        # debug info:
        #print(event, swemper_data)

        # if event in (None, 'EXIT'):
        if event == "EXIT" or event == sg.WIN_CLOSED:
            break
        elif event == '//COPY':
            log("//COPY")
            clipboard.copy(swemper_data['thebasename'])
            l = len(swemper_data['thebasename'])
            print(f'\n++ Copied {l} chars to clipboard')
        elif event == '//WRITE':
            log("//WRITE")
            OUTPUT_FILE = yaml_basename+'.yaml'
            try:
                with open(OUTPUT_FILE, 'w') as fp:
                    fp.write(yaml_data)
            except Exception as e:
                print(f"-- Error: {e}")
            else:
                l = len(yaml_data.split(sep='\n'))
                print(f'\n++ Wrote {l} lines as "{OUTPUT_FILE}"')

        elif event == '//UPDATE':
            log('//UPDATE')
            # Update the textbox element
            # to be the value of "input" element
            basename = swemper_data['SwemperSeriesID'] + \
                "_"+swemper_data['YearPublished']
            yaml_basename = basename
            if swemper_data['PeriodicalVolIdx']:
                basename = basename+"_vol" + \
                    swemper_data['PeriodicalVolIdx'].zfill(3)
            if swemper_data['PeriodicalNrIdx']:
                basename = basename+"_nr" + \
                    swemper_data['PeriodicalNrIdx'].zfill(3)

            # calc md5 from filename (with available fields minus extension) and use as unique swemper-vol-id
            # log(basename)
            md5 = hashlib.md5(basename.encode('utf-8')).hexdigest()

            window['//WRITE'].Update(disabled=False)
            # window['//WRITE'].update(mouseov)
            sd = swemper_data
            yaml_data = f"""\
%YAML 1.2
---
Swemper-yaml-filename: {yaml_basename}.yaml
Swemper-volume-descriptor:
    # PRE-FLIGHT
    SwemperSeriesID: &ssid {sd['SwemperSeriesID']}
    FullPeriodicalName: !!str {sd['FullPeriodicalName']}
    PeriodicalVolIdx: &vol !!str {sd['PeriodicalVolIdx']}
    PeriodicalNrIdx: &nr !!str {sd['PeriodicalNrIdx']}
    YearPublished: &yr {sd['YearPublished']}
    BaseFilename: 
        - *ssid
        - *yr
        - *vol
        - *nr
    Swemper-vol-id: {md5}
    # POST-FLIGHT:
    NumberOfScannedPages: {sd['NumberOfScannedPages']}
    FinalPrintedPageNumber: {sd['FinalPrintedPageNumber']}
    DateOfScan: {sd['DateOfScan']}
    Comment: {sd['Comment']}
...
"""
            window['textbox'].update(yaml_data)
            window['thebasename'].update(basename+"_")

    # Outside event loop, EXIT #
    window.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: appname.py swemperfilename.yaml")
        # sys.exit(
    main()
