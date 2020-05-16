#!/usr/bin/env python3
from uisetting import UISetting
import PySimpleGUI as sg
import time
import client as ct

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
		client = ct.Client()
		client.start()
		client.runningloop.wait()
		client.connect_to_server()
		client.register((self.id, self.keyword))
		return client

