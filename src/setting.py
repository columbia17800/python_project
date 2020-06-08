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
				bo = check_exit()
				if bo:
					break
			if event == '-Save-':
				self.update_setting(values)
			if event == '-Cancel-' :
				break
			if event == '-Reset-':
				self.reset_setting()
				break

	def update_setting(self, values):
		self.setting.themecolor = values[0]
		self.window_font_size = values[1]
		self.window_font_color = values[2]
		self.window_font = value[3]

	def reset_setting(self):
		self.setting.themecolor = 'GreenTan'
		self.window_font_size = '12'
		self.window_font_color = 'Black'
		self.window_font = 'Helvetica'

	def check_exit():
		lay = [[sg.Text('Do you want to exit? Your setting would not be saved!')]
				[sg.Button('Exit'), sg.Button('Back')]]
		win = sg.Window('Exit', lay)

		while True:
			event, values = win.read():
			if event == 'Exit':
				return True
			if event in (None, 'Back'):
				return False
		win.close()

	def __del__(self):
		self.window.close()