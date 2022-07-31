#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from PIL import Image, ImageDraw, ImageFont
import time

import RPi.GPIO as GPIO
from SH1106 import SH1106, config
import pins

from .oled_keyboard import keyboard
import .oled_menu

from .interface import DisplayInterface, CancelInput

class Display(DisplayInterface):
	def __init__(self, *args):
		super().__init__(*args)
		pins.init()
		self.__display = SH1106()
		self.__display.Init()
		self.__display.clear()
		self.scale = 11

	def __del__(self):
		self.__display.clear()

	def display(self) -> None:
		self.__display.ShowImage(self.__display.getbuffer(self.image))

	def clear(self) -> None:
		self.image = Image.new('1', (self.disp.width, self.disp.height), "WHITE")
		self.draw = ImageDraw.Draw(image)
		self.__display.clear()

	def get(self, hidden: bool = False) -> str:
		keys = keyboard(__display)
		keys.hidden = hidden
		keys.draw(True)

		MENU_EXIT = False
		MENU_FAILED = False

		def menu_back(_ = None):
			if keys.text == '':
				MENU_FAILED = True
				MENU_EXIT = True
			else:
				keys.backspace()

		def menu_fwd(_ = None):
			MENU_EXIT = True

		GPIO.add_event_detect(pins.KEY_LEFT, GPIO.FALLING, callback=keys.left, bouncetime=200)
		GPIO.add_event_detect(pins.KEY_RIGHT, GPIO.FALLING, callback=keys.right, bouncetime=200)
		GPIO.add_event_detect(pins.KEY_UP, GPIO.FALLING, callback=keys.up, bouncetime=200)
		GPIO.add_event_detect(pins.KEY_DOWN, GPIO.FALLING, callback=keys.down, bouncetime=200)
		GPIO.add_event_detect(pins.KEY_PRESS, GPIO.FALLING, callback=keys.select, bouncetime=250)
		GPIO.add_event_detect(pins.KEY1, GPIO.FALLING, callback=keys.toggleShift, bouncetime=250)
		GPIO.add_event_detect(pins.KEY2, GPIO.FALLING, callback=menu_fwd, bouncetime=250)
		GPIO.add_event_detect(pins.KEY3, GPIO.FALLING, callback=menu_back, bouncetime=250)

		while not MENU_EXIT:
			time.sleep(0.1)

		GPIO.remove_event_detect(pins.KEY_LEFT)
		GPIO.remove_event_detect(pins.KEY_RIGHT)
		GPIO.remove_event_detect(pins.KEY_UP)
		GPIO.remove_event_detect(pins.KEY_DOWN)
		GPIO.remove_event_detect(pins.KEY_PRESS)
		GPIO.remove_event_detect(pins.KEY1)
		GPIO.remove_event_detect(pins.KEY2)
		GPIO.remove_event_detect(pins.KEY3)

		if MENU_FAILED:
			raise CancelInput
		else:
			return keys.text

	def put(self, row: int, text: str, *, bold: bool = False, italics: bool = False, inverted: bool = False, is_option: bool = False) -> None:
		self.draw.text((1, row * self.scale), text, font=ImageFont.load_default(), fill=int(inverted))

# def menu(menu_item: dict) -> int:
# 	global __display
# 	global MENU_EXIT
# 	global MENU_FAILED
#
# 	title = variables.parse(menu_item['title']) if 'title' in menu_item else ''
#
# 	options = build_options(menu_item)
#
# 	menu = oled_menu.oled_menu(__display)
# 	menu.options(options, title)
# 	menu.display()
#
# 	MENU_FAILED = False
# 	MENU_EXIT = False
#
# 	def menu_back(_ = None):
# 		global MENU_EXIT
# 		global MENU_FAILED
# 		MENU_EXIT = True
# 		MENU_FAILED = True
#
# 	def menu_fwd(_ = None):
# 		global MENU_EXIT
# 		if any(k in menu.select() for k in ('input', 'action', 'return', 'goto')):
# 			MENU_EXIT = True
#
# 	GPIO.add_event_detect(pins.KEY_LEFT, GPIO.FALLING, callback=menu_back, bouncetime=200)
# 	GPIO.add_event_detect(pins.KEY_RIGHT, GPIO.FALLING, callback=menu_fwd, bouncetime=200)
# 	GPIO.add_event_detect(pins.KEY_UP, GPIO.FALLING, callback=menu.up, bouncetime=200)
# 	GPIO.add_event_detect(pins.KEY_DOWN, GPIO.FALLING, callback=menu.down, bouncetime=200)
# 	GPIO.add_event_detect(pins.KEY_PRESS, GPIO.FALLING, callback=menu_fwd, bouncetime=250)
#
# 	while not MENU_EXIT:
# 		time.sleep(0.1)
#
# 	GPIO.remove_event_detect(pins.KEY_LEFT)
# 	GPIO.remove_event_detect(pins.KEY_RIGHT)
# 	GPIO.remove_event_detect(pins.KEY_UP)
# 	GPIO.remove_event_detect(pins.KEY_DOWN)
# 	GPIO.remove_event_detect(pins.KEY_PRESS)
#
# 	__display.clear()
#
# 	if MENU_FAILED:
# 		raise CancelInput
# 	else:
# 		return menu.select()
#
# def message(text: str, title: str = '') -> None:
# 	global __display
# 	image = Image.new('1', (__display.width, __display.height), "WHITE")
# 	draw = ImageDraw.Draw(image)
# 	draw.text((1,0), text, font=ImageFont.load_default(), fill=0)
# 	__display.ShowImage(__display.getbuffer(image))
