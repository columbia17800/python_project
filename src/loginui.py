#!/usr/bin/env python3
try:
	from .uisetting import UISetting
	from . import client as ct
except:
	from uisetting import UISetting
	import client as ct
import PySimpleGUI as sg
import time

'''
methods in client:

请求链接服务器（登录：namepair里面是用户名和密码，用户名在前
connect_to_server(namepair: Tuple[str, str]):				call to connect to server
注册：namepair要不是单独用户名，就是用户名和密码
	单独用户名只会raise,但可以检测出用户名是否重复
register(namepair: Tuple[str,] or Tuple[str, str]):			register this user into server
捡朋友：从listui里选id作为friendname，请求p2p连接
pick_a_friend(friendname: str):					pick a friend in friend list that is about to call on
'''

class LogUI():
	def __init__(self):
		sg.theme('DarkAmber')
		self.setup()
		layout = [sg.Text("Your id: "), sg.Input(size = (12, 1), key = "ID"),
					sg.Text("Your password: "), sg.Input(size = (12, 1), key = "PASSWORD"),
					sg.Button("Log In"), sg.Button("Sign Up"), sg.Button("Exit")]
		window = sg.Window("Log in to chat!", layout)
		
	def event_loop(self):
		while True:
			event, values = window.read()
			user = (values['-ID-'], values['-PASSWORD-'])
			if event is None:
				break
			if event == 'Log In':
				client.connect_to_server(user)
			if event == 'Sign up':
				client.register(user)
			if event == 'Exit':
				break


	def setup(self):
		raise NotImplementedError 
