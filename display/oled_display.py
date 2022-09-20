#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#Before doing anything, make sure the SPI device exists!
from pathlib import Path
import time

def CHECK_FOR_SPI():
    SPI = Path('/dev/spidev0.0')
    if not SPI.exists():
        print('Waiting for SPI interface to come online...')
        for i in range(30):
            time.sleep(1)
            if SPI.exists():
                return

        print('SPI interface did not load in time. Exiting.')
        exit(1)

CHECK_FOR_SPI()


from PIL import Image, ImageDraw, ImageFont
import asyncio

import RPi.GPIO as GPIO
from .SH1106 import SH1106, config, pins

from .oled_keyboard import Keyboard

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
		self.__in_display = False

	def cleanup(self) -> None:
		blank_image = Image.new('1', (self.max_width(), self.max_height()), 'WHITE')
		self.__display.ShowImage(self.__display.getbuffer(blank_image))

	def max_height(self) -> int:
		return self.__display.height

	def max_width(self) -> int:
		return self.__display.width

	def text_scale(self) -> int:
		return 11

	def line_scale(self) -> int:
		return 3 # need some spacing on either side of the line

	async def display(self) -> None:
		while self.__in_display:
			await asyncio.sleep(0)

		self.__in_display = True
		self.__display.ShowImage(self.__display.getbuffer(self.image))
		self.__in_display = False

	async def display_nothing(self) -> None:
		blank_image = Image.new('1', (self.max_width(), self.max_height()), 'WHITE')
		self.__display.ShowImage(self.__display.getbuffer(blank_image))

	def clear(self) -> None:
		self.image = Image.new('1', (self.max_width(), self.max_height()), 'WHITE')
		self.draw = ImageDraw.Draw(self.image)

	async def get(self, hidden: bool = False) -> str:
		keys = Keyboard(self)
		keys.hidden = hidden
		await keys.show()

		self.menu_failed = False
		self.menu_exited = False

		async def menu_fail():
			if keys.text == '':
				self.menu_failed = True
			else:
				await keys.backspace()

		def menu_exit(_ = None):
			self.menu_exited = True

		GPIO.add_event_detect(pins.KEY_LEFT, GPIO.FALLING, callback=lambda _: asyncio.run(keys.left()), bouncetime=200)
		GPIO.add_event_detect(pins.KEY_RIGHT, GPIO.FALLING, callback=lambda _: asyncio.run(keys.right()), bouncetime=200)
		GPIO.add_event_detect(pins.KEY_UP, GPIO.FALLING, callback=lambda _: asyncio.run(keys.up()), bouncetime=200)
		GPIO.add_event_detect(pins.KEY_DOWN, GPIO.FALLING, callback=lambda _: asyncio.run(keys.down()), bouncetime=200)
		GPIO.add_event_detect(pins.KEY_PRESS, GPIO.FALLING, callback=lambda _: asyncio.run(keys.select()), bouncetime=250)
		GPIO.add_event_detect(pins.KEY1, GPIO.FALLING, callback=lambda _: asyncio.run(keys.toggleShift()), bouncetime=250)
		GPIO.add_event_detect(pins.KEY2, GPIO.FALLING, callback=menu_exit, bouncetime=250)
		GPIO.add_event_detect(pins.KEY3, GPIO.FALLING, callback=lambda _: asyncio.run(menu_fail()), bouncetime=250)

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

	def put(self, y_pos: int, _text: str, *, bold: bool = False, italics: bool = False, inverted: bool = False, is_option: bool = False) -> None:
		if y_pos < 0:
			y_pos = self.max_height() - self.text_scale() + (y_pos + 1)

		if inverted:
			self.rect(
				bounds = (
					(0, y_pos),
					(self.max_width(), y_pos + self.text_scale())
				),
				fill = False
			)
		self.draw.text((1, y_pos), _text, font=self.__font, fill=int(inverted))

	def text(self, x: int, y:int, _text: str, *, bold: bool = False, italics: bool = False, inverted: bool = False) -> None:
		if x < 0:
			x = self.max_width() - len(_text) * (self.text_scale() - 4) + (x + 1)

		if y < 0:
			y = self.max_height() - self.text_scale() + (y + 1)

		if inverted:
			self.rect(
				bounds = (
					(x, y),
					(x + self.text_scale() - 3, y + (len(_text) * self.text_scale()))
				),
				fill = False
			)
		self.draw.text((x+1, y), _text, font = self.__font, fill=int(inverted))

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

		async def toggle_display_sleep():
			self.display_sleeping = not self.display_sleeping
			if self.display_sleeping:
				GPIO.remove_event_detect(pins.KEY_LEFT)
				GPIO.remove_event_detect(pins.KEY_RIGHT)
				GPIO.remove_event_detect(pins.KEY_UP)
				GPIO.remove_event_detect(pins.KEY_DOWN)
				GPIO.remove_event_detect(pins.KEY_PRESS)
				await self.display_nothing()
			else:
				GPIO.add_event_detect(pins.KEY_LEFT, GPIO.FALLING, callback=menu_fail, bouncetime=200)
				GPIO.add_event_detect(pins.KEY_RIGHT, GPIO.FALLING, callback=menu_exit, bouncetime=200)
				GPIO.add_event_detect(pins.KEY_UP, GPIO.FALLING, callback=lambda _: asyncio.run(self.menu_move_up()), bouncetime=200)
				GPIO.add_event_detect(pins.KEY_DOWN, GPIO.FALLING, callback=lambda _: asyncio.run(self.menu_move_down()), bouncetime=200)
				GPIO.add_event_detect(pins.KEY_PRESS, GPIO.FALLING, callback=menu_exit, bouncetime=250)
				await self.display()

		def menu_fail(_ = None):
			self.menu_failed = True

		def menu_exit(_ = None):
			self.menu_exited = True

		await toggle_display_sleep()
		GPIO.add_event_detect(pins.KEY1, GPIO.FALLING, callback=lambda _: asyncio.run(toggle_display_sleep()), bouncetime=200)

		while not (self.menu_exited or self.menu_failed):
			await asyncio.sleep(0.1)

		await toggle_display_sleep()
		GPIO.remove_event_detect(pins.KEY1)

		if self.menu_failed:
			raise CancelInput
		else:
			return
