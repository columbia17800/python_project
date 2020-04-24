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
		
		while True:
			event, value = window.read()
			if event in (None, 'EXIT'):
				break
			if event == 'SEND':
				query = value['-QUERY-'].restrip()
				now = time.asctime(time.localtime(time.time()))
				print(now)
				print('you:')
				print(format(query))
				# send message here
			# new if for receive message

		window.close