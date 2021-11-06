#!/usr/bin/python
# -*- coding:utf-8 -*-

import RPi.GPIO as GPIO
import time, traceback, subprocess
from PIL import Image, ImageDraw, ImageFont

import SH1106.SH1106 as SH1106
import SH1106.config as config

import textMenu
import keyboard
import pins

MENU_EXIT = False

try:
	pins.init()
	disp = SH1106.SH1106()

	print("1.3inch OLED")
	# Initialize library.
	disp.Init()
	# Clear display.
	disp.clear()

	"""
	menu = textMenu.textMenu(disp)
	menu.options((
		'Keyboard',
		'Exit',
	));
	menu.draw(True)

	# Menu selection
	holding = False
	while True:
		keyPin = -1

		if not GPIO.input(KEY_UP_PIN):
			menu.up()
			keyPin = KEY_UP_PIN
		if not GPIO.input(KEY_DOWN_PIN):
			menu.down()
			keyPin = KEY_DOWN_PIN
		if not (GPIO.input(KEY_RIGHT_PIN) and GPIO.input(KEY_PRESS_PIN)):
			if menu.terminal():
				if menu.path() == 'Exit':
					disp.clear()
					exit()
				if menu.path() == 'Keyboard':
					menu.draw(False)
					break
			menu.select()
			keyPin = KEY_RIGHT_PIN
		if not GPIO.input(KEY_LEFT_PIN):
			menu.back()
			keyPin = KEY_LEFT_PIN

		# Delay menu selections on key press
		if keyPin > -1:
			menuDelay = True
			for i in range(0,10):
				time.sleep(0.01)
				if GPIO.input(keyPin):
					menuDelay = False
					holding = False
					break
			if menuDelay:
				if holding:
					time.sleep(0.02)
				else:
					time.sleep(0.5)

				holding = False if GPIO.input(keyPin) else True
	"""

	# Show keyboard
	keys = keyboard.keyboard(disp)
	keys.hidden = True
	keys.draw(True)



	def menu_back(_=None):
		global MENU_EXIT
		if keys.text == '':
			MENU_EXIT = True
		else:
			keys.backspace()

	def menu_fwd(_=None):
		global MENU_EXIT
		print(">>"+keys.text)
		MENU_EXIT = True

	GPIO.add_event_detect(pins.KEY_LEFT, GPIO.FALLING, callback=keys.left, bouncetime=200)
	GPIO.add_event_detect(pins.KEY_RIGHT, GPIO.FALLING, callback=keys.right, bouncetime=200)
	GPIO.add_event_detect(pins.KEY_UP, GPIO.FALLING, callback=keys.up, bouncetime=200)
	GPIO.add_event_detect(pins.KEY_DOWN, GPIO.FALLING, callback=keys.down, bouncetime=200)
	GPIO.add_event_detect(pins.KEY_PRESS, GPIO.FALLING, callback=keys.select, bouncetime=250)
	GPIO.add_event_detect(pins.KEY1, GPIO.FALLING, callback=keys.toggleShift, bouncetime=250)
	GPIO.add_event_detect(pins.KEY2, GPIO.FALLING, callback=menu_fwd, bouncetime=250)
	GPIO.add_event_detect(pins.KEY3, GPIO.FALLING, callback=menu_back, bouncetime=250)

	while True:
		if MENU_EXIT: break
		time.sleep(0.1)

	"""
	holding = False
	while True:
		keyPin = -1

		if not GPIO.input(pins.KEY1):
			keys.toggleShift()
			keyPin = pins.KEY1
		if not GPIO.input(pins.KEY2):
			print(keys.text)
			break
		if not GPIO.input(pins.KEY3):
			if keys.text == '': break
			keys.backspace()
			keyPin = pins.KEY3
		if not GPIO.input(pins.KEY_RIGHT):
			keys.right()
			keyPin = pins.KEY_RIGHT
		if not GPIO.input(pins.KEY_LEFT):
			keys.left()
			keyPin = pins.KEY_LEFT
		if not GPIO.input(pins.KEY_UP):
			keys.up()
			keyPin = pins.KEY_UP
		if not GPIO.input(pins.KEY_DOWN):
			keys.down()
			keyPin = pins.KEY_DOWN
		if not GPIO.input(pins.KEY_PRESS):
			keys.select()
			keyPin = pins.KEY_PRESS

		# Delay menu selections on key press
		if keyPin > -1:
			menuDelay = True
			for i in range(0,10):
				time.sleep(0.01)
				if GPIO.input(keyPin):
					menuDelay = False
					holding = False
					break
			if menuDelay:
				if holding:
					time.sleep(0.02)
				else:
					time.sleep(0.5)

				holding = False if GPIO.input(keyPin) else True

	"""

	disp.clear()

except IOError as e:
	print(e)

except KeyboardInterrupt:
	print("ctrl + c:")
	disp.clear()
	exit()
