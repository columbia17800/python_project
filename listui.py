#!/usr/bin/env python3
from uisetting import UISetting
import PySimpleGUI as sg
import time

class ListUI():
	def __init__(self, namelist):
		layout = [[sg.Text('List of users')],
			[sg.Input(size = (20, 1), enable_events = True, key = '-INPUT-')],
			[sg.Listbox(namelist, size = (20, 4), key = '-LIST-')],
			[sg.Button('Chat!'), sg.Button('Exit')]]
	
		self.window = sg.Window('Choose someone to chat!', layout)

	def event_loop(self):
		while True:
			event, values = self.window.read()
			if event in (None, 'Exit'):
				break
			if values['-INPUT-'] != '':
				wanted = values['-INPUT-']
				targets = [x for x in namelist if search in x]
				self.window['-LIST-'].update(targets)
			else:
				self.window['-LIST-'].update(namelist)
			if event == 'Chat!':
				that = values['-LIST-'][0]
				that = that + '!'
				print("Start chating with", that)
				# Start chating here

	def __del__(self):
		self.window.close()