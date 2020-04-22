#!/usr/bin/env python3
import PySimepleGUI as sg
from typing import List,Dict,Tuple,Any,NoReturn

class UISetting():
	def __init__(self):
		self.theme_color = 'GreenTan'
		self.window_font = 'Helvetica'
		self.window_font_size = ' 12'
		self.button_size = (8,2)
		self.text_words = 'Your output will enter here'
		self.text_size = (40,1)
		self.output_size = (100, 20)
		self.output_font = ('Helvetica 10')
		self.multiline_size = (70, 5)
		self.multiline_enter_submits = True
		self.multiline_key = '-QUERY-'
		self.do_not_clear = False
		self.Buttons = []					#list of Buttons(tuples)
	def setUpButton(type: str, color: Tuple, bind_return: bool) -> NoReturn:
		# append new Button to list
		self.Buttons.append(
			sg.Button(type, button_color=color, bind_return_key=bind_return)
			)

	# a menu bar at the top of the window
	def setUpMenuBar() -> NoReturn:
		menu_def = [['File', ['Open', 'Save', 'Exit',]],
                ['Edit', ['Paste', ['Special', 'Normal',], 'Undo'],],
                ['Help', 'About...'],]
		self.menu = [sg.Menu(menu_def, tearoff=False)]

	def setUpButtonMenu() -> NoReturn:
		right_click_menu = ['Unused', ['Right', '!&Click', '&Menu', 'E&xit', 'Properties']]
		self.buttonMenu.append([sg.ButtonMenu, right_click_menu, key='-BMENU-', sg.Button('Plain Button')]


