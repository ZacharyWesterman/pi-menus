#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import oled_display as display
import json
import time
import variables
import subprocess

if __name__ == '__main__':
	try:
		display.start()

		with open('menu.json', 'r') as fp:
			menu_display = json.load(fp)

		menus = ['main']
		# display.put('input: ', 0, 0)
		# result = display.get()

		while True:
			this_menu = menu_display[menus[-1]]
			try:
				display.message('Loading...')
				this_option = display.menu(this_menu)

				if 'input' in this_option:
					value = display.get('password' in this_option['input'] and this_option['input']['password'])
					variables.set('line', this_option['text'])
					variables.set('item', this_option['text'].split())
					value = variables.set(this_option['input']['var'], value)

				if 'action' in this_option:
					try:
						display.message('Processing...')
						subprocess.check_output(this_option['action'], shell=True)
					except:
						pass

				if 'return' in this_option and this_option['return']:
					menus = menus[:-1]
					if not len(menus): break
				elif 'goto' in this_option:
					menus += [this_option['goto']]
			except display.CancelInput:
				menus = menus[:-1]
				if not len(menus): break

			time.sleep(0.1)

			# print(menus)

		display.stop()
		exit()

	except KeyboardInterrupt:
		display.stop()
		print("User signalled interrupt. Exiting.")
		exit()

	except Exception as e:
		display.stop()
		raise e
