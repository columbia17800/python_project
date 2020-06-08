#!/usr/bin/env python3
try:
	from .uisetting import UISetting
	from .chatui import ChatUI
except:
	from uisetting import UISetting
	from chatui import ChatUI
import PySimpleGUI as sg
import time

QT_ENTER_KEY1 = 'special 16777220'
QT_ENTER_KEy2 = 'special 16777221'

class ListUI():
	def __init__(self, setting: UISetting, namelist, id):
		layout = [[sg.Text('List of users')],
			[sg.Input(size = (20, 1), enable_events = True, key = '-INPUT-')],
			[sg.Listbox(namelist, size = (20, 4), key = '-LIST-')],
			[sg.Button('Chat!'), sg.Button('Exit'), sg.Button('Setting')]]
	
		self.namelist = namelist
		self.window = sg.Window('Choose someone to chat!', layout)
		self.setting = setting

	def event_loop(self) -> str:
		while True:
			event, values = self.window.read()
			key = pygame
			// 多加一个if，当好友发来聊天请求时call check_connect，返回true则开始聊天。
			if event in (None, 'Exit'):
				break
			if values['-INPUT-'] != '':
				wanted = values['-INPUT-']
				targets = [x for x in namelist if search in x]
				self.window['-LIST-'].update(targets)
			else:
				self.window['-LIST-'].update(self.namelist)
			if event == 'Chat!':
				that = values['-LIST-'][0]
				print("Start chating with", that + '!')
				# Start chating here
				return that
			if event in ('\r', QT_ENTER_KEY1, QT_ENTER_KEY2):
				that = values['-LIST-'][0]
				print("Start chating with", that + '!')
				return that
			if event == 'Setting':
				print('Setting!')

	def check_connect(self, friend) -> bool:
		asking = friend + ' is asking to chat with you!'
		lay = [[sg.Text(asking)]
			[sg.Button('Accept'), sg.Button('Reject')]]

		win = window('Chat request', lay)

		while True:
			event, values = win.read()
			if event in (None, 'Reject'):
				return False
			if event == 'Accept':
				return True
		win.close()

	def pop_chat(self, friend: str):
		chat = self.client.pick_a_friend(friend)
		chatui = ChatUI(self.setting, chat)
		chatui.start()

	def __del__(self):
		self.window.close()