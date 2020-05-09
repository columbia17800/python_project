#!/usr/bin/env python3
from uisetting import UISetting
from typing import NoReturn, Union, Optional, Tuple
from chat import Chatter
from collections import deque
import PySimpleGUI as sg
import time
import asyncio
import random
import string
import threading

class ExitError(Exception):
	pass

class ChatUI():
	def __init__(self, set: UISetting, chatter: Chatter):
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
		
	async def recv_msg(self) -> NoReturn:
		while not self.exit:
			async with self.chatter.recv_signal as crs:
				crs.wait()
				(ver, seq, data) = self.chatter.recv_msg.popleft()
				self.chatter.base[seq].remove(ver)
				print( data )
				self.recv_msg_box.append( data )

	async def handle_send(self):
		raise NotImplementedError

	async def handle_receive(self):
		raise NotImplementedError

	async def event_loop(self):
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

				await asyncio.sleep(1)
		finally:
			# close the window
			self.window.close()
			# wait for all tasks
			tasks = asyncio.all_tasks()
			for task in tasks:
				task.cancel()

	def manage(self):
