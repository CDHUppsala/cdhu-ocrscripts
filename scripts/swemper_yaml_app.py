import PySimpleGUI as sg
#import textwrap

basename = ""
yaml_basename = ""
yaml_data = ""

sg.theme('DarkBlue2')
try:
    sg.set_options(font=("Menlo", 16))
    #sg.set_options(font=("Fira Code", 16))
    #sg.set_options(font=("Monoid HalfTight Regular", 16))
except:
    sg.set_options(font=("Courier", 16)); print("No fancy monospaced font. Use Courier as fallback.")

col0 = [
            [  #row 0
                sg.Text("SwemperSeriesID:"), 
                sg.Input(key='SwemperSeriesID', default_text="Status")
            ], # row 1
            [
                sg.Text("FullPeriodicalName:"), 
                sg.Input(key='FullPeriodicalName', default_text="Status")
            ],
            [
                sg.Text("PeriodicalVolIdx:"), 
                sg.Input(key='PeriodicalVolIdx')
            ],
            [
                sg.Text("PeriodicalNrIdx:"), 
                sg.Input(key='PeriodicalNrIdx')
            ],
            [
                sg.Text("YearPublished:"), 
                sg.Input(key='YearPublished', default_text="1958")
            ],
            [
                sg.Text("Base filename to copy:"), 
                sg.Input(key='thebasename', default_text="<Copy this>")
            ],
            [
                sg.Button('Print'), 
                sg.Button('//COPY'), 
                sg.Button('//WRITE'), 
                sg.Button('Exit'),
            ],
            [  #last row
                sg.Multiline(size=(50,80),expand_y=True, key='textbox')
            ],
          ]


#TEMPLATE FOR GUI COLUMN
# colNN = [
#     [sg.Text("row 1"), sg.Text("row 1"), sg.Text("row 1")],  # Row 0
#     [sg.Text("row 2"), sg.Text("row 2"), sg.Text("row 2")],  # Row 1
#     [sg.Text("row 3"), sg.Text("row 2"), sg.Text("row m")],  # Row m
# ]

string1=""" ____ ____ ____ ____ __________
||C |||D |||H |||U |||       
||__|||__|||__|||__|||_________
|/__\|/__\|/__\|/__\|/_________

 SWEMPER TOOL 𝛼 / INSTRUCTIONS:
"""
info = "...instructions and info......instructions and info......instructions and info......instructions and info......instructions and info......instructions and info..."
print(info)
col4 = [
    [sg.Text(string1,p=0)],  # Row 0
    [sg.Text(info,p=0, size=(38, 20))],  # Row 1

]

layout = [
            [sg.Column(col0,size=(500,600),pad=(5,10)), sg.Column(col4,vertical_alignment='t',pad=0)]
        ]

window = sg.Window('Swemper YAML Tool', layout, size=(800, 600), resizable=True)
  
while True:
    event, swemper_data = window.read()
    print(event, swemper_data)

    #These updates need to happen in main event loop. Not sure why.
    basename = swemper_data['SwemperSeriesID']+"_"+swemper_data['YearPublished']
    yaml_basename = basename
    if swemper_data['PeriodicalVolIdx']:
        basename = basename+"_vol"+swemper_data['PeriodicalVolIdx'].zfill(3)
    if swemper_data['PeriodicalNrIdx']:
        basename = basename+"_nr"+swemper_data['PeriodicalNrIdx'].zfill(3)

    if event in  (None, 'Exit'):
        break
    
    if event == 'Print':
        # Update the textbox  element
        # to be the value of "input" element
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
  Swemper-vol-id: 
...
"""
    window['textbox'].update(yaml_data)
    window['thebasename'].update(basename+"_")
  
window.close()