#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import subprocess, time
import curses

import variables

from enum import Enum
class message(Enum):
	text = 1
	password = 2

class CancelInput(Exception):
	def __init__(self):
		super().__init__('Unhandled user-input "cancel" action.')

__terminal = None

def start() -> None:
	global __terminal
	__terminal = curses.initscr()
	__terminal.nodelay(True)
	curses.noecho()
	curses.cbreak()
	curses.curs_set(0)

def stop() -> None:
	global __terminal
	curses.nocbreak()
	__terminal.keypad(False)
	curses.echo()
	curses.endwin()
	curses.curs_set(1)

def clear() -> None:
	global __terminal
	__terminal.erase()

def put(text, x, y) -> None:
	global __terminal
	__terminal.addstr(y, x, text)
	__terminal.refresh()

def get(hidden: bool = True) -> str:
	global __terminal
	curses.curs_set(1)

	startx = __terminal.getyx()[1]

	#Poll for input
	text = ''
	while True:
		# If input from terminal, use that.
		c = __terminal.getch()
		if c != curses.ERR:
			if c == ord('\n'):
				break
			elif c == 27: # Escape characters
				cmd = [__terminal.getch(), __terminal.getch()]
				if cmd[0] == curses.ERR: # ESCAPE key
					curses.curs_set(0)
					raise CancelInput
			elif c == 127: #BACKSPACE
				yx = __terminal.getyx()
				if yx[1] > startx:
					text = text[:-1]
					__terminal.addch(yx[0], yx[1]-1, ' ')
					__terminal.move(yx[0], yx[1]-1)
					__terminal.refresh()
			else:
				text += chr(c)
				__terminal.addch('*' if hidden else chr(c))
				__terminal.refresh()

			continue

		time.sleep(0.05)

	curses.curs_set(0)
	return text

def __print_menu(options: list, title: str = '') -> None:
	global __terminal

	yx = __terminal.getyx()
	__terminal.move(0,0)

	if title:
		__terminal.addstr(0, 0, title+'\n', curses.A_BOLD)

	for i in range(0, len(options)):
		if i == yx[0]:
			text = options[i]['alt'] if 'alt' in options[i] else options[i]['text']
			__terminal.addstr('> '+text+'\n', curses.A_REVERSE)
		else:
			text = options[i]['text']
			__terminal.addstr('> '+text+'\n')

	__terminal.move(yx[0], yx[1])
	__terminal.refresh()

def __parse_menu_option(option: dict) -> dict:
	new_opt = {}
	for i in option:
		if type(option[i]) is str:
			new_opt[i] = variables.parse(option[i])
		elif type(option[i]) is dict:
			new_opt[i] = __parse_menu_option(option[i])
		else:
			new_opt[i] = option[i]

	return new_opt

def build_options(menu_item: dict) -> list:
	options = []

	for option in menu_item['options']:
		options += [__parse_menu_option(option)]

	# If there's a template (for dynamic lists), build it and add to options
	if 'template' in menu_item:
		var = menu_item['template']['var']
		value = variables.get(var)
		variables.set(var, value)
		for line in value.split('\n'):
			variables.set('line', line)
			variables.set('item', line.split())
			for option in menu_item['template']['options']:
				options += [__parse_menu_option(option)]

	return options


def menu(menu_item: dict) -> int:
	global __terminal

	title = variables.parse(menu_item['title']) if 'title' in menu_item else ''


	options = build_options(menu_item)
	__print_menu(options, title)

	while True:
		y = __terminal.getyx()[0]
		c = [__terminal.getch(), __terminal.getch(), __terminal.getch()]
		if c[0] == ord('\n'):
			clear()
			return y #index of chosen option
		elif c[0] == 27: # Escape characters
			#Navigate menu
			if c[2] == 66 and y < (len(options) - 1):
				__terminal.move(y + 1, 0) #Move up
			elif c[2] == 65 and y > 0:
				__terminal.move(y - 1, 0) #Move down
			elif c[2] == 67:
				clear()
				return y #index of chosen option
			elif c[2] == 68:
				clear()
				raise CancelInput
			elif c[1] == curses.ERR:
				clear()
				raise CancelInput

			__print_menu(options, title)
			continue

		time.sleep(0.05)

	raise "Menu reached an invalid state!"

def message(text: str, title: str = '') -> None:
	pass
