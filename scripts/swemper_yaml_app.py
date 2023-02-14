#!/usr/bin/env python3
# Author: ML/authorfunction
import hashlib
import sys
import os
import requests
import re
import pprint
# from cprint import *
# from PIL import Image
from datetime import date
from weakref import finalize
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
|/__\\|/__\\|/__\\|/__\\|/_____________

SWEMPER METADATA TOOL 𝛼/ver / HINTS:
"""
new_info_string = """
___________________________________

Centre for                 :: ::
                        :: :: :: ::
Digital Humanities         :: :: ::
                        :: :: ::
Uppsala / CDHU
_______________________ .. .. .. ..

SWEMPER METADATA TOOL 𝛼/ver / HINTS:"""

info = '''1) Fill in pre-flight fields. Copy filename and paste into scanner-software.
2) Operate the scanner.
3) Fill in post-flight fields.
'''

left_info_string = """
_______________________

Centre for
Digital Humanities
Uppsala / CDHU
_______________________"""

new_info_string = """
SWEMPER METADATA TOOL 𝛼/ver / HINTS:
"""

swemper_data = {}


def log(s, level='default'):
    if level == 'default':
        # print(s)
        sg.cprint(s)
    elif level == 'info':
        sg.cprint(s, text_color='yellow')
    elif level == 'ok':
        sg.cprint(s, text_color='green')
    elif level == 'error':
        sg.cprint(s, text_color='red')
    elif level == 'warning':
        sg.cprint(s, text_color='pink')
    elif DEBUG and level == 'debug':
        sg.cprint('DEBUG:' + s, text_color='white')


def get_cwd():
    log("++ Current work directory is: " + os.getcwd())


def init_layout():
    sg.theme('DarkBlue2')
    try:
        sg.set_options(font=("IBM Plex Mono", 14))
        # sg.set_options(font=("Menlo", 14))
        # sg.set_options(font=("UbuntuMono Nerd Font", 17))
        # sg.set_options(font=("Inconsolata", 17))
        # sg.set_options(font=("Source Code Pro ExtraLight Regular", 16))
        # sg.set_options(font=("Fira Code", 16)) #/Users/mattslindstrom/Downloads/Monoid-HalfTight-Dollar-0/Monoid-Retina-HalfTight-Dollar-0.ttf
        # sg.set_options(font=("Monoid HalfTight Regular", 16))
    except BaseException:
        log('-- Falling back to Courier', level='warning')
        sg.set_options(font=("Courier", 16))
        # print("//No fancy monospaced font available. Use Courier as fallback.")

    tab0 = [

        [  # row 0
            sg.Text("SwemperSeriesID:", auto_size_text=True),
            sg.Input(key='SwemperSeriesID',
                     default_text="", expand_x=True)
        ],  # row 1
        [
            sg.Text("FullPeriodicalName:"),
            sg.Input(key='FullPeriodicalName',
                     default_text="", expand_x=True)
        ],
        [
            sg.Text("PeriodicalVolIdx:"),
            sg.Input(key='PeriodicalVolIdx', expand_x=True)
        ],
        [
            sg.Text("PeriodicalNrIdx:"),
            sg.Input(key='PeriodicalNrIdx', expand_x=True)
        ],
        [   # ...row n
            sg.Text("YearPublished:"),
            sg.Input(key='YearPublished',
                     default_text="", expand_x=True)
        ],
        [   # ...row n
            sg.Text("LibrisTitle:"),
            sg.Input(key='LibrisTitle',
                     default_text="", expand_x=True)
        ],
        [   # ...row n
            sg.Text("LibrisISSN:"),
            sg.Input(key='LibrisISSN',
                     default_text="", expand_x=True)
        ],
        [   # ...row n
            sg.Text("LibrisURL:"),
            sg.Input(key='LibrisURL',
                     default_text="", expand_x=True)
        ],
        [   # ...final row
            sg.Text("LibrisID:"),
            sg.Input(key='LibrisID',
                     default_text="", expand_x=True)
        ],

    ]

    tab1 = [

        [  # row 0
            sg.Text("NumberOfScannedPages:"),
            sg.Input(key='NumberOfScannedPages',
                     default_text="", expand_x=True)
        ],  # row 1
        [  # row 0
            sg.Text("FirstPrintedPageNumber:"),
            sg.Input(key='FirstPrintedPageNumber',
                     default_text="", expand_x=True)
        ],  # row 1
        [
            sg.Text("FinalPrintedPageNumber:"),
            sg.Input(key='FinalPrintedPageNumber',
                     default_text="", expand_x=True)
        ],
        [
            sg.Text("DateOfScan:"),
            sg.Input(key='DateOfScan',
                     default_text=date.today().isoformat(), expand_x=True)
        ],
        [
            sg.Text("Comment:"),
            # sg.Input(key='Comment', expand_x=True)
            # Use this instead for multiline field:
            sg.Multiline(
                size=(
                    2, 4), expand_y=True, key='Comment', expand_x=True, p=(
                    (0, 5), (0, 0)))  # , no_scrollbar=True)
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
        [  # BUTTON ROW 0
            sg.Button('UPDATE YAML', key='//UPDATE',
                      bind_return_key=True, p=((0, 0), (20, 10))),
            sg.Button('COPY F-NAME', key='//COPY', p=((5, 0), (20, 10))),
            sg.Button('OPEN', key='//OPEN', p=((5, 0), (20, 10))),
            sg.Button('PATH', key='//SETPATH', p=((5, 0), (20, 10))),
            sg.Button('WRITE YAML', key='//WRITE',
                      disabled=False, p=((5, 0), (20, 10))),
            sg.Button('EXIT', key='EXIT', p=((5, 0), (20, 10))),
        ],
        [  # BUTTON ROW 1
            sg.Button('SEARCH LIBRIS', key='//XSEARCH',
                      disabled=False, p=((0, 0), (0, 10))),
            sg.Button('PARSE LIBRIS-ID', key='//LIBRISPARSE',
                      disabled=False, p=((5, 0), (0, 10))),
            sg.Button('CLR STDOUT', key='//CLEARSTDOUT',
                      disabled=False, p=((5, 0), (0, 10))),
            sg.Button('TIMESTAMP', key='//TIMESTAMP',
                      disabled=False, p=((5, 0), (0, 10))),
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

        [sg.Text(left_info_string, p=0), sg.Image('./cdhu-symbol-white.png', subsample=16,
                                                  p=((18, 0 + 10), (28 + 0, 0)),), ],  # row 0
        [sg.Text(new_info_string, p=0, size=(0, 0))],  # Row 0
        [sg.Text(info, p=0, size=(36, 10))],  # Row 1
        [sg.Multiline('-- stdout --\n', key='stdout', p=10, size=(380, HEIGHT / 2),
                      reroute_stdout=True,
                      reroute_cprint=True,
                      autoscroll=True)],  # Row 2

    ]

    layout = [
        [
            sg.Column(col0, size=(WIDTH / 2 + (WIDTH / 12), HEIGHT),
                      # sg.Column(col0,
                      expand_x=True, expand_y=True, pad=(15, 10)),  # left col


            sg.Column(col1, justification='right', element_justification='right',
                      vertical_alignment='bottom', pad=0)  # right col
            # sg.Column(col1)  # right col
        ]
    ]
    return layout


def read_yaml_file(file, window):
    with open(file) as f:
        yaml = YAML()
        yaml_file_data = yaml.load(f)
        fields = [
            'SwemperSeriesID',
            'FullPeriodicalName',
            'PeriodicalVolIdx',
            'PeriodicalNrIdx',
            'YearPublished',
            'LibrisTitle',
            'LibrisISSN',
            'LibrisURL',
            'LibrisID',
            'NumberOfScannedPages',
            'FirstPrintedPageNumber',
            'FinalPrintedPageNumber',
            'DateOfScan',
            'Comment']
        for field in fields:
            # clear all fields as we are opening a new file.
            window[field].update('')
            log(f'++ Cleared "{field}".')
        log(f'++ Reading yaml...', level='info')
        for field in fields:
            try:
                window[field].update(
                    yaml_file_data['Swemper-volume-descriptor'][field])
            except BaseException:
                log('No data/field: ' + field, level='warning')

        log('++ Done reading ' + file, level='ok')


def update_yaml(window, swemper_data):
    # Update the textbox element
    # to be the value of "input" element
    # Caclulate base filename etc
    # NB! Pressing enter in any field calls this code as well -- reason: bind_return_key=True is set for this button above
    # TODO: There's room for improvement here with error checking etc
    # Also, currently there might be inconstistencies/bugs in how this
    # works visavi bind_return_key...

    # Globals have to be declared inside functions. This pythonism was severly
    # confusing to an old C-programmer...
    global yaml_data
    global basename
    global yaml_basename

    fix_colon = swemper_data['FullPeriodicalName']
    fix_colon = fix_colon.replace(" : ", ": ")
    window['FullPeriodicalName'].update(fix_colon)

    basename = swemper_data['SwemperSeriesID'] + \
        "_" + swemper_data['YearPublished']
    # Use this for lowercase basenames:
    # basename = basename.lower()
    yaml_basename = basename
    if swemper_data['PeriodicalVolIdx']:
        basename = basename + "_vol" + \
            swemper_data['PeriodicalVolIdx'].zfill(3)
    if swemper_data['PeriodicalNrIdx']:
        basename = basename + "_nr" + \
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
Swemper-yaml-filename: {basename}.yaml
Swemper-volume-descriptor:
    # PRE-FLIGHT
    SwemperSeriesID: &ssid {sd['SwemperSeriesID']}
    FullPeriodicalName: !!str "{sd['FullPeriodicalName']}"
    PeriodicalVolIdx: &vol !!str {sd['PeriodicalVolIdx']}
    PeriodicalNrIdx: &nr !!str {sd['PeriodicalNrIdx']}
    YearPublished: &yr {sd['YearPublished']}
    BaseFilename:
        - *ssid
        - *yr
        - *vol
        - *nr
    Swemper-vol-id: {md5}
    LibrisTitle: {sd['LibrisTitle']}
    LibrisISSN: {sd['LibrisISSN']}
    LibrisURL: {sd['LibrisURL']}
    LibrisID: {sd['LibrisID']}
    #LibrisResource:
    # POST-FLIGHT:
    NumberOfScannedPages: {sd['NumberOfScannedPages']}
    FirstPrintedPageNumber: {sd['FirstPrintedPageNumber']}
    FinalPrintedPageNumber: {sd['FinalPrintedPageNumber']}
    DateOfScan: {sd['DateOfScan']}
    Comment: "{sd['Comment']}"
...
"""
    window['textbox'].update(yaml_data)
    window['thebasename'].update(basename + "_")
    log('++ Updated YAML-data.', level='ok')


def main():
    # Initialize and create GUI
    layout = init_layout()

    # ADDED finalize=True here to remove error message -- might cause
    # problems? Needs tesing.
    window = sg.Window('Swemper YAML Tool', layout,
                       size=(WIDTH, HEIGHT), resizable=True, finalize="True")
    log('Finished setting up layout.', level='debug')
    get_cwd()
    # Look for defaults-file and load
    try:
        log('++ Reading default.yaml...', level='info')
        read_yaml_file('default.yaml', window)
    except BaseException:
        log('-- Failed reading default.yaml', level='error')

    # MAIN EVENT LOOP #
    while True:
        event, swemper_data = window.read()
        # debug info:
        # print(event, swemper_data)

        # if event in (None, 'EXIT'):
        if event == "EXIT" or event == sg.WIN_CLOSED:
            break
        elif event == '//SETPATH':
            log('//SETPATH', level='debug')
            try:
                path = sg.popup_get_folder('', no_window=True)
                os.chdir(path)
                # log('Path is:'+path)
            except BaseException:
                log("-- No new path was set", level='warning')
            get_cwd()
        elif event == '//OPEN':
            log('//OPEN', level='debug')
            file = sg.popup_get_file('', no_window=True)
            try:
                read_yaml_file(file, window)
            except BaseException:
                log('Error opening file!', level='error')
        elif event == '//COPY':
            log("//COPY", level='debug')
            # TODO: PySimpleGUI actually has it's own clipboard function, so
            # might switched to that and remove a dependency.
            clipboard.copy(swemper_data['thebasename'])
            l = len(swemper_data['thebasename'])
            log(f'++ Copied {l} chars to clipboard', level='ok')
        elif event == '//WRITE':
            log("//WRITE", level='debug')
            # Call update_yaml() before writing
            update_yaml(window, swemper_data)
            # CHANGE: Changed to basename variable from basename_yaml to get
            # full names for yaml, files as this should make sense: One
            # yml-file for each physical scanned volume.
            global yaml_data
            global basename
            OUTPUT_FILE = basename + '.yaml'
            get_cwd()
            log('Filename: ' + OUTPUT_FILE)
            log('Data out:\n' + yaml_data)
            try:
                with open(OUTPUT_FILE, 'w') as fp:
                    fp.write(yaml_data)
            except Exception as e:
                log(f"-- Error: {e}", level='error')
            else:
                l = len(yaml_data.split(sep='\n'))
                log(f'++ Wrote {l} lines as "{OUTPUT_FILE}"', level='ok')
        elif event == '//XSEARCH':
            log(event, level='debug')
            log('++ Querying Libris with FullPeriodicalName.', level='info')
            try:
                records = 0
                url = f"https://libris.kb.se/xsearch?query=title:({swemper_data['FullPeriodicalName']})&format=json"
                r = requests.get(url)
                records = r.json().get("xsearch").get("records")
                log(f"++ Request URL: {url}")
                log(f"++ Found {records} in Libris.", level='ok')
                pprint.pprint(
                    r.json().get("xsearch").get("list"),
                    indent=1,
                    width=160)
            except BaseException:
                log(f"-- Error: Couldn't complete http-request.", level='error')
        elif event == '//LIBRISPARSE':
            log(event, level='debug')
            log('++ Parsing LibrisID field.', level='info')
            try:
                url = f"https://libris.kb.se/xsearch?query=onr:({swemper_data['LibrisID']})&format=json"
                r = requests.get(url)
                libris_title = r.json().get("xsearch").get("list")[
                    0].get("title")
                libris_issn = r.json().get("xsearch").get("list")[
                    0].get("issn")
                libris_url = r.json().get("xsearch").get("list")[
                    0].get("identifier")
                window['LibrisTitle'].update(libris_title)
                window['LibrisISSN'].update(libris_issn)
                window['LibrisURL'].update(libris_url)
                pprint.pprint(
                    r.json().get("xsearch").get("list"),
                    indent=1,
                    width=160)
            except BaseException:
                log("-- Failed parsing libris data.", level='error')
        elif event == '//CLEARSTDOUT':
            log(event, level='debug')
            window['stdout'].update('')
            # sg.cprint('++ Cleared stdout.', t='yellow')
            log('++ Cleared stdout.', level='ok')
        elif event == '//TIMESTAMP':
            log(event, level='debug')
            window['DateOfScan'].update(date.today().isoformat())
        elif event == '//UPDATE':
            log('//UPDATE', level='debug')
            update_yaml(window, swemper_data)

    # Outside event loop, EXIT #
    window.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: appname.py swemperfilename.yaml")
        # sys.exit(
    main()
