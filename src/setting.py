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
		layout = [[sg.Text("Background color"), sg.]
			]
		window = sg.Window("Time Tracker", layout,
			default_element_size=(12, 1),
          	text_justification='r',
          	auto_size_text=False,
          	auto_size_buttons=False,
          	default_button_element_size=(12, 1),
          	finalize=True)

	def event_loop(self) -> str:
		while True:
			event, values = self.window.read()
			key = pygame
			if event in (None, 'Exit'):
				break
			if values['-INPUT-'] != '':
				wanted = values['-INPUT-']
				targets = [x for x in namelist if search in x]
				self.window['-LIST-'].update(targets)
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