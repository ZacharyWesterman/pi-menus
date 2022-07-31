#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time
import curses

from .interface import DisplayInterface, CancelInput

class Display(DisplayInterface):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
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

	def max_height(self) -> int:
		return self.__terminal.getmaxyx()[0]

	def max_width(self) -> int:
		return self.__terminal.getmaxyx()[1]

	def text_scale(self) -> int:
		return 1

	def line_scale(self) -> int:
		return 1

	def display(self) -> None:
		self.__terminal.refresh()

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

	def put(self, y_pos: int, text: str, *, bold: bool = False, italics: bool = False, inverted: bool = False, is_option: bool = False) -> None:
		flags = 0
		if bold: flags += curses.A_BOLD
		if italics: flags += curses.A_ITALIC
		if inverted: flags += curses.A_REVERSE
		if is_option: text = f'> {text}'.ljust(self.max_width()-1)
		self.__terminal.addstr(y_pos, 0, text, flags)

	def hline(self, x_pos: int, y_pos: int, width: int) -> None:
		self.__terminal.hline(y_pos, x_pos, '-', width)

	def vline(self, x_pos: int, y_pos: int, height: int) -> None:
		self.__terminal.vline(y_pos, x_pos, '|', height)

	def rect(self, bounds: tuple, fill: bool) -> None:
		raise Exception('term_display.rect is not defined!')
		pass

	# def scrollbar(self, y_offset: int, item_index: int, total_items: int) -> None:
	# 	maxh = self.max_height()
	# 	maxw = self.max_width()
	# 	self.__terminal.vline(y_offset, maxw-3, ' ', maxh)
	# 	self.__terminal.vline(y_offset, maxw-2, ' ', maxh)
	# 	self.__terminal.vline(y_offset, maxw-1, ' ', maxh)
	#
	# 	# bar_pos = (maxh-y_offset) // total_items
	# 	bar_pos = item_index * (maxh-y_offset) // total_items
	# 	self.__terminal.vline(bar_pos+y_offset, maxw-2, '#', 1)

	def await_movement(self) -> None:
		while True:
			c = [self.__terminal.getch(), self.__terminal.getch(), self.__terminal.getch()]

			if c[0] == ord('\n'):
				return #An option has been selected
			elif c[0] == 27: # Escape characters
				#Navigate menu
				if c[2] == 65:
					self.scroll_up()
				elif c[2] == 66:
					self.scroll_down()
				elif c[2] == 67:
					return #An option has been selected
				elif c[2] == 68:
					raise CancelInput
				elif c[1] == curses.ERR:
					raise CancelInput

				continue

			time.sleep(0.05)
