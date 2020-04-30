#!/usr/bin/env python3
from uisetting import UISetting
import PySimpleGUI as sg
import time

class LogUI():
	def __init__(self, set: UISetting):
		sg.theme('DarkAmber')
		id = sg.popup_get_text('Type in a cool =ID here')
		# if ID exist then return FAIL
		if id == '':
			print('Null ID!')
		# else return id to the server
