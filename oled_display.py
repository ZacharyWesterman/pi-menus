#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from PIL import Image, ImageDraw, ImageFont
import time

import RPi.GPIO as GPIO
import SH1106.SH1106 as SH1106
import SH1106.config as config
import pins

import variables
import keyboard
import oled_menu

from enum import Enum
class message(Enum):
	text = 1
	password = 2

class CancelInput(Exception):
	def __init__(self):
		super().__init__('Unhandled user-input "cancel" action.')

__display = None

def start() -> None:
	global __display
	pins.init()
	__display = SH1106.SH1106()
	__display.Init()
	__display.clear()

def stop() -> None:
	global __display
	__display.clear()

def clear() -> None:
	global __display
	__display.clear()

def put(text, x, y) -> None:
	global __terminal
	__terminal.addstr(y, x, text)
	__terminal.refresh()

def get(hidden: bool = False) -> str:
	global __display
	keys = keyboard.keyboard(__display)
	keys.hidden = hidden
	keys.draw(True)

	MENU_EXIT = False
	MENU_FAILED = False
	def menu_back(_ = None):
		if keys.text == '':
			MENU_EXIT = True
		else:
			keys.backspace()

	def menu_fwd(_ = None):
		MENU_FAILED = True
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
	global __display

	title = variables.parse(menu_item['title']) if 'title' in menu_item else ''

	options = build_options(menu_item)

	menu = oled_menu.oled_menu(__display)
	menu.options(options, title)
	menu.display()

	MENU_FAILED = False
	MENU_EXIT = False

	def menu_back(_ = None):
		MENU_EXIT = True
		MENU_FAILED = True

	def menu_fwd(_ = None):
		if any(k in menu.select() for k in ('input', 'action', 'return', 'goto')):
			MENU_EXIT = True

	GPIO.add_event_detect(pins.KEY_LEFT, GPIO.FALLING, callback=menu_fwd, bouncetime=200)
	GPIO.add_event_detect(pins.KEY_RIGHT, GPIO.FALLING, callback=menu_back, bouncetime=200)
	GPIO.add_event_detect(pins.KEY_UP, GPIO.FALLING, callback=menu.up, bouncetime=200)
	GPIO.add_event_detect(pins.KEY_DOWN, GPIO.FALLING, callback=menu.down, bouncetime=200)
	GPIO.add_event_detect(pins.KEY_PRESS, GPIO.FALLING, callback=menu_fwd, bouncetime=250)

	while not MENU_EXIT:
		time.sleep(0.1)

	GPIO.remove_event_detect(pins.KEY_LEFT)
	GPIO.remove_event_detect(pins.KEY_RIGHT)
	GPIO.remove_event_detect(pins.KEY_UP)
	GPIO.remove_event_detect(pins.KEY_DOWN)
	GPIO.remove_event_detect(pins.KEY_PRESS)

	__display.clear()

	if MENU_FAILED:
		raise CancelInput
	else:
		return menu.select()

def message(text: str, title: str = '') -> None:
	clear()
	put(text, 0, 0)
