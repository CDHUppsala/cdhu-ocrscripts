import PySimpleGUI as sg
import pyperclip as clipboard
import hashlib
#import textwrap

basename = ""
yaml_basename = ""
yaml_data = ""
DEBUG = True

def log(s):
    if DEBUG:
        print(s)

sg.theme('DarkBlue2')
try:
    sg.set_options(font=("Menlo", 16))
    #sg.set_options(font=("Source Code Pro ExtraLight Regular", 16))
    #sg.set_options(font=("Fira Code", 16)) #/Users/mattslindstrom/Downloads/Monoid-HalfTight-Dollar-0/Monoid-Retina-HalfTight-Dollar-0.ttf
    #sg.set_options(font=("Monoid HalfTight Regular", 16))
except:
    sg.set_options(font=("Courier", 16)); print("No fancy monospaced font. Use Courier as fallback.")

col0 = [
            [  #row 0
                sg.Text("SwemperSeriesID:"), 
                sg.Input(key='SwemperSeriesID', default_text="Status",expand_x=True)
            ], # row 1
            [
                sg.Text("FullPeriodicalName:"), 
                sg.Input(key='FullPeriodicalName', default_text="Status",expand_x=True)
            ],
            [
                sg.Text("PeriodicalVolIdx:"), 
                sg.Input(key='PeriodicalVolIdx',expand_x=True)
            ],
            [
                sg.Text("PeriodicalNrIdx:"), 
                sg.Input(key='PeriodicalNrIdx',expand_x=True)
            ],
            [
                sg.Text("YearPublished:"), 
                sg.Input(key='YearPublished', default_text="1958",expand_x=True)
            ],
            [
                sg.Text("Base filename to copy:"), 
                sg.Input(key='thebasename', default_text="<Copy this>",expand_x=True)
            ],
            [
                sg.Button('//UPDATE'), 
                sg.Button('//COPY'), 
                sg.Button('//WRITE'), 
                sg.Button('EXIT'),
            ],
            [  #last row
                sg.Multiline(size=(50,80),expand_y=True, key='textbox',expand_x=True)
            ],
          ]


#TEMPLATE FOR GUI COLUMN
# colNN = [
#     [sg.Text("row 1"), sg.Text("row 1"), sg.Text("row 1")],  # Row 0
#     [sg.Text("row 2"), sg.Text("row 2"), sg.Text("row 2")],  # Row 1
#     [sg.Text("row 3"), sg.Text("row 2"), sg.Text("row m")],  # Row m
# ]

string1=""" ____ ____ ____ ____ ______________
||C |||D |||H |||U |||       
||__|||__|||__|||__|||_____________
|/__\|/__\|/__\|/__\|/_____________

 SWEMPER TOOL 𝛼/ver / INSTRUCTIONS:
"""
info = "...instructions and info......instructions and info......instructions and info......instructions and info......instructions and info......instructions and info..."
print(info)
col4 = [
    [sg.Text(string1,p=0)],  # Row 0
    [sg.Text(info,p=0, size=(38, 20))],  # Row 1

]
WIDTH=1000
HEIGHT=800
layout = [
            [
                sg.Column(col0,size=(WIDTH/2,HEIGHT),expand_x=True,pad=(15,10)), #left col
                sg.Column(col4,justification='right',element_justification='left',vertical_alignment='top',pad=0) #right col
            ]
        ]

window = sg.Window('Swemper YAML Tool', layout, size=(WIDTH, HEIGHT), resizable=True)

# Main event loop starts
while True:
    event, swemper_data = window.read()
    #debug info:
    print(event, swemper_data)
    
    #if event in (None, 'EXIT'):
    if event == "EXIT" or event == sg.WIN_CLOSED:
        break
    elif event == '//COPY':
        log("//COPY")
        log(swemper_data['thebasename'])
        clipboard.copy(swemper_data['thebasename'])
    elif event == '//WRITE':
        log("//WRITE not implemented")
        current_text=window['textbox']
        window['textbox'].update(current_text.get()+'\n++Warning: //WRITE not implemented.')
    elif event == '//UPDATE':
        # Update the textbox element
        # to be the value of "input" element
        basename = swemper_data['SwemperSeriesID']+"_"+swemper_data['YearPublished']
        yaml_basename = basename
        if swemper_data['PeriodicalVolIdx']:
            basename = basename+"_vol"+swemper_data['PeriodicalVolIdx'].zfill(3)
        if swemper_data['PeriodicalNrIdx']:
            basename = basename+"_nr"+swemper_data['PeriodicalNrIdx'].zfill(3)

        #calc md5 from filename (with available fields minus extension) and use as unique swemper-vol-id
        log(basename)
        md5 = hashlib.md5(basename.encode('utf-8')).hexdigest()

        yaml_data = f"""\
%YAML 1.2
---
Swemper-yaml-filename: {yaml_basename}.yaml
Swemper-volume-descriptor:
  SwemperSeriesID: &ssid {swemper_data['SwemperSeriesID']}
  FullPeriodicalName: !!str {swemper_data['FullPeriodicalName']}
  PeriodicalVolIdx: &vol !!str {swemper_data['PeriodicalVolIdx']}
  PeriodicalNrIdx: &nr !!str {swemper_data['PeriodicalNrIdx']}
  YearPublished: &yr {swemper_data['YearPublished']}
  BaseFilename: 
    - *ssid
    - *yr
    - *vol
    - *nr
  Swemper-vol-id: {md5}
...
"""
        window['textbox'].update(yaml_data)
        window['thebasename'].update(basename+"_")

# Outside event loop, EXIT: 
window.close()