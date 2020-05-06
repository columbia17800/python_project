#!/usr/bin/env python3
from uisetting import UISetting
from typing import NoReturn, Union, Optional, Tuple
import PySimpleGUI as sg
import time
import chat

class ExitError(Exception):
	pass

class ChatUI():
	def __init__(self, set: UISetting, chatter: chat.Chatter):
		title = sg.Text(set.text_words, size = set.text_size)
		layout = [[title], [sg.Output(size = set.output_size, font = set.output_font)],
			[sg.Multiline(size = set.multiline_size, enter_submits=set.multiline_enter_submits, 
				key = set.multiline_key, do_not_clear = set.do_not_clear),
			sg.Button(set.Buttons[0]),
			sg.Button(set.Buttons[1])]]
		
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

	async def handler(self, event, value):
		if event in (None, 'EXIT'):
			self.exit = True
		elif event == 'SEND':
			query = value['-QUERY-'].restrip()
			local = time.localtime(time.time())
			if local[3] != self.start[3]:
				now = time.asctime(local)
				print(now)
			elif local[4] - start[4] >= 5:
				now = time.asctime(local)
				print(now)
			print('you:')
			print(format(query))
			start = local
			# send message here
		# new if for receive message
		elif event == 'receive':
			# print message
			raise NotImplementedError
		else:
			raise NotImplementedError

	async def event_loop(self):
		try:
			while not self.exit:
				event, value = self.window.read()
				tasks.append( asyncio.create_task( self.handler(event, value)) )
		finally:
			# close the window
			self.window.close()
			# wait for all tasks
			tasks = asyncio.all_tasks()
			asyncio.gather(*tasks)