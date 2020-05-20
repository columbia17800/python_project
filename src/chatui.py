#!/usr/bin/env python3
try:
	from uisetting import UISetting
	from typing import NoReturn, Union, Optional, Tuple
	from chat import Chatter
except:
	from .uisetting import UISetting
	from .typing import NoReturn, Union, Optional, Tuple
	from .chat import Chatter
from collections import deque
from threading import Thread
import PySimpleGUI as sg
import time
import asyncio
import random
import string


class ExitError(Exception):
	pass

class ChatUI(Thread):
	def __init__(self, set: UISetting, chatter: Chatter):
		Thread.__init__(self)
		title = sg.Text(set.text_words, size = set.text_size)
		layout = [[title], [sg.Output(size = set.output_size, font = set.output_font)],
			[sg.Multiline(size = set.multiline_size, enter_submits=set.multiline_enter_submits, 
				key = set.multiline_key, do_not_clear = set.do_not_clear),
			set.Buttons[0],
			set.Buttons[1]]]
		
		self.window = sg.Window(1, layout, font = (set.window_font, set.window_font_size), default_button_element_size = set.button_size)
		self.start = time.localtime(time.time())
		self.chatter = chatter
		self.exit = False
		self.msg_box = deque()
		self.recv_msg_box = deque()
		
	def run(self):
		self.event_loop()

	def recv_msg(self) -> Optional[str]:
		if len(self.recv_msg_box) != 0:
			return self.recv_msg_box.popleft()
		return None

	def send_msg(self, msg: str):
		self.chatter.import_msg(msg)

	def event_loop(self):
		try:
			while True:
				event, value = self.window.read()
				if event in (None, 'EXIT'):
					self.exit = True
					break
				elif event == 'SEND':
					query = value['-QUERY-'].rstrip()
					local = time.localtime(time.time())
					if local[3] != self.start[3]:
						now = time.asctime(local)
						print(now)
					elif local[4] - self.start[4] >= 5:
						now = time.asctime(local)
						print(now)
					print('you:')
					print(format(query))
					self.start = local
					# send message here
				# new if for receive message
				elif event == 'receive':
					# print message
					raise NotImplementedError
				else:
					raise NotImplementedError
		finally:
			# close the window
			self.window.close()
			# wait for all tasks and cancel them
			raise NotImplementedError