#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time
import curses

from enum import Enum
class message(Enum):
	text = 1
	password = 2

class CancelInput(Exception):
	def __init__(self):
		super().__init__('Unhandled user-input "cancel" action.')

class Display:
	def __init__(self, variable_handler: object):
		self.variables = variable_handler
		self.__terminal = curses.initscr()
		self.__terminal.nodelay(True)
		curses.noecho()
		curses.cbreak()
		curses.curs_set(0)

	def __del__(self):
		curses.nocbreak()
		self.__terminal.keypad(False)
		curses.echo()
		curses.endwin()
		curses.curs_set(1)

	def clear(self) -> None:
		self.__terminal.erase()

	def get(self, hidden: bool = False) -> str:
		curses.curs_set(1)

		startx = self.__terminal.getyx()[1]

		#Poll for input
		text = ''
		while True:
			# If input from terminal, use that.
			c = self.__terminal.getch()
			if c != curses.ERR:
				if c == ord('\n'):
					break
				elif c == 27: # Escape characters
					cmd = [self.__terminal.getch(), self.__terminal.getch()]
					if cmd[0] == curses.ERR: # ESCAPE key
						curses.curs_set(0)
						raise CancelInput
				elif c == 127: #BACKSPACE
					yx = self.__terminal.getyx()
					if yx[1] > startx:
						text = text[:-1]
						self.__terminal.addch(yx[0], yx[1]-1, ' ')
						self.__terminal.move(yx[0], yx[1]-1)
						self.__terminal.refresh()
				else:
					text += chr(c)
					self.__terminal.addch('*' if hidden else chr(c))
					self.__terminal.refresh()

				continue

			time.sleep(0.05)

		curses.curs_set(0)
		return text

	def __print_menu(self, options: list, title: str = '') -> None:
		yx = self.__terminal.getyx()
		self.__terminal.move(0,0)

		if title:
			self.__terminal.addstr(0, 0, title+'\n', curses.A_BOLD)

		for i in range(0, len(options)):
			if i == yx[0]:
				text = options[i]['alt'] if 'alt' in options[i] else options[i]['text']
				self.__terminal.addstr('> '+text+'\n', curses.A_REVERSE)
			else:
				text = options[i]['text']
				self.__terminal.addstr('> '+text+'\n')

		self.__terminal.move(yx[0], yx[1])
		self.__terminal.refresh()

	def __parse_menu_option(self, option: dict) -> dict:
		new_opt = {}
		for i in option:
			if type(option[i]) is str:
				new_opt[i] = self.variables.parse(option[i])
			elif type(option[i]) is dict:
				new_opt[i] = self.__parse_menu_option(option[i])
			else:
				new_opt[i] = option[i]

		return new_opt

	def build_options(self, menu_item: dict) -> list:
		options = []

		for option in menu_item['options']:
			options += [self.__parse_menu_option(option)]

		# If there's a template (for dynamic lists), build it and add to options
		if 'template' in menu_item:
			var = menu_item['template']['var']
			value = self.variables.get(var)
			self.variables.set(var, value)
			for line in value.split('\n'):
				self.variables.set('line', line)
				items = line.split()
				items += [''] * (10 - len(items))
				self.variables.set('item', items)
				for option in menu_item['template']['options']:
					options += [self.__parse_menu_option(option)]

		return options


	def menu(self, menu_item: dict) -> dict:
		title = self.variables.parse(menu_item['title']) if 'title' in menu_item else ''

		options = self.build_options(menu_item)
		self.__print_menu(options, title)

		while True:
			y = self.__terminal.getyx()[0]
			c = [self.__terminal.getch(), self.__terminal.getch(), self.__terminal.getch()]

			if c[0] == ord('\n'):
				self.clear()
				return options[y] #chosen option
			elif c[0] == 27: # Escape characters
				#Navigate menu
				if c[2] == 66 and y < (len(options) - 1):
					self.__terminal.move(y + 1, 0) #Move up
				elif c[2] == 65 and y > 0:
					self.__terminal.move(y - 1, 0) #Move down
				elif c[2] == 67:
					#if this option does anything
					if any(k in options[y] for k in ('input', 'action', 'return', 'goto')):
						self.clear()
						return options[y] #then return the chosen option
				elif c[2] == 68:
					self.clear()
					raise CancelInput
				elif c[1] == curses.ERR:
					self.clear()
					raise CancelInput

				self.__print_menu(options, title)
				continue

			time.sleep(0.05)

		raise Exception("Menu reached an invalid state!")

	def message(self, text: str, title: str = '') -> None:
		self.clear()
		self.__terminal.addstr(0, 0, text)
		self.__terminal.refresh()
