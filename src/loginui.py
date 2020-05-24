#!/usr/bin/env python3
try:
	from uisetting import UISetting
	import client as ct
except:
	from .uisetting import UISetting
	from . import client as ct
import PySimpleGUI as sg
import time

class LogUI():
	def __init__(self):
		sg.theme('DarkAmber')
		id = sg.popup_get_text('Type in a cool =ID here')
		# if ID exist then return FAIL
		self.id = id
		self.keyword = None
		if id == '':
			print('Null ID!')
		# else return id to the server
		else:
			return id

	def connect_server(self):
		client.register((self.id, self.keyword))
		return client

