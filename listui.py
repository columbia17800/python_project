#!/usr/bin/env python3
from settings import UISetting
import PySimpleGUI as sg
import time

class ListUI():
	def __init__(self, set: UISetting, namelist):
		layout = [[sg.Text('List of users')],
			[sg.Input(size = (20, 1), enable_events = True, key = '-INPUT-')],
			[sg.Listbox(namelist, size = (20, 4), key = '-LIST-')],
			[sg.Button('Chat!'), sg.Button('Exit')]]
	
	window = sg.Window('Choose someone to chat!', layout)

	while True:
		event, values = window.read()
		if event in (None, 'Exit'):
			break
		if values['-INPUT-'] != '':
			wanted = values['-INPUT-']
			targets = [x for x in namelist if search in x]
			window['-LIST-'].update(targets)
		else:
			window['-LIST-'].update(namelist)
		if event == 'Chat!':
			that = values['-LIST-'][0]
			that = that + '!'
			print("Start chating with", that)
			# Start chating here

	def __del__(self):
		window.close()