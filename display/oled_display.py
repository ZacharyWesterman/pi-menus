#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from PIL import Image, ImageDraw, ImageFont
import asyncio

import RPi.GPIO as GPIO
from .SH1106 import SH1106, config, pins

from .oled_keyboard import keyboard

from .interface import DisplayInterface, CancelInput

class Display(DisplayInterface):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		pins.init()
		self.__display = SH1106()
		self.__display.Init()
		self.__display.clear()
		self.scale = 11
		self.__font = ImageFont.load_default()

	def __del__(self):
		self.__display.clear()

	def max_height(self) -> int:
		return self.__display.height

	def max_width(self) -> int:
		return self.__display.width

	def text_scale(self) -> int:
		return 11

	def line_scale(self) -> int:
		return 3 # need some spacing on either side of the line

	def display(self) -> None:
		self.__display.ShowImage(self.__display.getbuffer(self.image))

	def clear(self) -> None:
		self.image = Image.new('1', (self.max_width(), self.max_height()), 'WHITE')
		self.draw = ImageDraw.Draw(self.image)

	async def get(self, hidden: bool = False) -> str:
		keys = keyboard(self.__display)
		keys.hidden = hidden
		keys.draw(True)

		self.menu_failed = False
		self.menu_exited = False

		def menu_fail(_ = None):
			if keys.text == '':
				self.menu_failed = True
			else:
				keys.backspace()

		def menu_exit(_ = None):
			self.menu_exited = True

		GPIO.add_event_detect(pins.KEY_LEFT, GPIO.FALLING, callback=keys.left, bouncetime=200)
		GPIO.add_event_detect(pins.KEY_RIGHT, GPIO.FALLING, callback=keys.right, bouncetime=200)
		GPIO.add_event_detect(pins.KEY_UP, GPIO.FALLING, callback=keys.up, bouncetime=200)
		GPIO.add_event_detect(pins.KEY_DOWN, GPIO.FALLING, callback=keys.down, bouncetime=200)
		GPIO.add_event_detect(pins.KEY_PRESS, GPIO.FALLING, callback=keys.select, bouncetime=250)
		GPIO.add_event_detect(pins.KEY1, GPIO.FALLING, callback=keys.toggleShift, bouncetime=250)
		GPIO.add_event_detect(pins.KEY2, GPIO.FALLING, callback=menu_exit, bouncetime=250)
		GPIO.add_event_detect(pins.KEY3, GPIO.FALLING, callback=menu_fail, bouncetime=250)

		while not (self.menu_exited or self.menu_failed):
			await asyncio.sleep(0.1)

		GPIO.remove_event_detect(pins.KEY_LEFT)
		GPIO.remove_event_detect(pins.KEY_RIGHT)
		GPIO.remove_event_detect(pins.KEY_UP)
		GPIO.remove_event_detect(pins.KEY_DOWN)
		GPIO.remove_event_detect(pins.KEY_PRESS)
		GPIO.remove_event_detect(pins.KEY1)
		GPIO.remove_event_detect(pins.KEY2)
		GPIO.remove_event_detect(pins.KEY3)

		if self.menu_failed:
			raise CancelInput
		else:
			return keys.text

	def put(self, y_pos: int, text: str, *, bold: bool = False, italics: bool = False, inverted: bool = False, is_option: bool = False) -> None:
		self.rect(
			bounds = (
				(0, y_pos),
				(self.max_width(), y_pos + self.text_scale())
			),
			fill = not inverted
		)
		self.draw.text((1, y_pos), text, font=self.__font, fill=int(inverted))

	def rect(self, bounds: tuple, fill: bool) -> None:
		self.draw.rectangle(bounds, fill = int(fill))

	def hline(self, x_pos: int, y_pos: int, width: int) -> None:
		self.draw.line([
			(x_pos, y_pos + 1),
			(x_pos + width, y_pos + 1)
		], fill=0)

	def vline(self, x_pos: int, y_pos: int, height: int) -> None:
		self.draw.line([
			(x_pos + 1, y_pos),
			(x_pos + 1, y_pos + height)
		], fill=0)


	async def await_movement(self) -> None:
		self.menu_failed = False
		self.menu_exited = False
		self.display_sleeping = True

		def toggle_display_sleep(_ = None):
			self.display_sleeping = not self.display_sleeping
			if self.display_sleeping:
				GPIO.remove_event_detect(pins.KEY_LEFT)
				GPIO.remove_event_detect(pins.KEY_RIGHT)
				GPIO.remove_event_detect(pins.KEY_UP)
				GPIO.remove_event_detect(pins.KEY_DOWN)
				GPIO.remove_event_detect(pins.KEY_PRESS)
				self.clear()
			else:
				GPIO.add_event_detect(pins.KEY_LEFT, GPIO.FALLING, callback=menu_fail, bouncetime=200)
				GPIO.add_event_detect(pins.KEY_RIGHT, GPIO.FALLING, callback=menu_exit, bouncetime=200)
				GPIO.add_event_detect(pins.KEY_UP, GPIO.FALLING, callback=lambda _: self.scroll_up(), bouncetime=200)
				GPIO.add_event_detect(pins.KEY_DOWN, GPIO.FALLING, callback=lambda _: self.scroll_down(), bouncetime=200)
				GPIO.add_event_detect(pins.KEY_PRESS, GPIO.FALLING, callback=menu_exit, bouncetime=250)
				self.display()

		def menu_fail(_ = None):
			self.menu_failed = True

		def menu_exit(_ = None):
			self.menu_exited = True

		toggle_display_sleep()
		GPIO.add_event_detect(pins.KEY1, GPIO.FALLING, callback=toggle_display_sleep, bouncetime=200)

		while not (self.menu_exited or self.menu_failed):
			await asyncio.sleep(0.1)

		toggle_display_sleep()
		GPIO.remove_event_detect(pins.KEY1)

		if self.menu_failed:
			raise CancelInput
		else:
			return
#
# def message(text: str, title: str = '') -> None:
# 	global __display
# 	image = Image.new('1', (__display.width, __display.height), "WHITE")
# 	draw = ImageDraw.Draw(image)
# 	draw.text((1,0), text, font=ImageFont.load_default(), fill=0)
# 	__display.ShowImage(__display.getbuffer(image))
