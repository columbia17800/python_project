#!/usr/bin/env python3
from uisetting import UISetting
import PySimpleGUI as sg
import time

QT_ENTER_KEY1 = 'special 16777220'
QT_ENTER_KEy2 = 'special 16777221'

class ListUI():
	def __init__(self, namelist, id):
		layout = [[sg.Text('List of users')],
			[sg.Input(size = (20, 1), enable_events = True, key = '-INPUT-')],
			[sg.Listbox(namelist, size = (20, 4), key = '-LIST-')],
			[sg.Button('Chat!'), sg.Button('Exit'), sg.Button('Setting')]]
	
		self.namelist = namelist
		self.window = sg.Window('Choose someone to chat!', layout)

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