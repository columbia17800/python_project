#!/usr/bin/env python3
from settings import UISetting
import PySimpleGUI as sg
import time

class ChatUI():
	def __init__(self, set: UISetting, thisID, thatID):
		title = sg.Text(set.text_words, size = set.text_size)
		layout = [[title], [sg.Output(size = set.output_size, font = set.output_font)],
			[sg.Multiline(size = set.multiline_size, enter_submits=set.multiline_enter_submits, 
				key = set.multiline_key, do_not_clear = set.do_not_clear)
			sg.Button(set.Buttons[0])
			sg.Button(set.Buttons[1])]]
		
		window = sg.Window(thatID, layout, font = (set.window_font, set.window_font_size), default_button_element_size = set.button_size)
		start = time.localtime(time.time())
		
		while True:
			event, value = window.read()
			if event in (None, 'EXIT'):
				break
			if event == 'SEND':
				query = value['-QUERY-'].restrip()
				local = time.localtime(time.time())
				if local[3] != start[3]:
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
			if event == 'receive':
				# print message
				


	def __del__(self):
		window.close()