#!/usr/bin/env python3
try:
	from .uisetting import uisetting
except:
	from uisetting import UISetting
import PySimpleGUI as sg
import time

QT_ENTER_KEY1 = 'special 16777220'
QT_ENTER_KEy2 = 'special 16777221'

class SettingUI():
	def __init__(self, setting: UISetting, namelist, id):
		self.setting = setting
		layout = [[sg.Text("Background color"), sg.OptionMenu(values = ('Green', 'Blue'), size = (20, 1))]
				[sg.Text("Font size"), sg.OptionMenu(values = ('Small', 'Middle', 'Large'), size = (20, 1))]
				[sg.Text("Font color"), sg.OptionMenu(values = ('Black', 'Brown'), size = (20, 1))]
				[sg.Text("Font type"), sg.OptionMenu(values = ('Helvetica', 'Calibri'), size = (20, 1))]
				[sg.Button('Save', button_color=('white', 'black'), key='-Save-'),
           		sg.Button('Cancel', button_color=('white', 'black'), key='-Cancel-'),
           		sg.Button('Reset', button_color=('white', 'firebrick3'), key='-Reset-'),
           		sg.Button('Exit', button_color=('white', 'springgreen4'), key='-Exit-')]
			]
		self.window = sg.Window("Settings", layout,
			default_element_size=(12, 1),
          	text_justification='r',
          	auto_size_text=False,
          	auto_size_buttons=False,
          	default_button_element_size=(12, 1),
          	finalize=True)

	def getSetting(self) -> UISetting:
		return self.setting

	def event_loop(self) -> str:
		while True:
			event, values = self.window.read()
			if event == sg.WIN_CLOSED:
        		break
			if event in (None, 'Exit'):
				break
			if event == 'Save':
				
			else:
				self.window['-LIST-'].update(self.namelist)
			if event == 'Chat!' or event == :
				that = values['-LIST-'][0]
				print("Start chating with", that + '!')
				# Start chating here
				return that
			if event in ('\r', QT_ENTER_KEY1, QT_ENTER_KEY2):
				that = values['-LIST-'][0]
				print("Start chating with", that + '!')
				return that

	def __del__(self):
		self.window.close()