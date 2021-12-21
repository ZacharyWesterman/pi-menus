#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import display
import json
import time
import variables

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
				result = display.menu(this_menu)
				this_option = display.build_options(this_menu)[result]

				if 'input' in this_option:
					value = display.get('password' in this_option['input'] and this_option['input']['password'])
					variables.set('line', this_option['text'])
					variables.set('item', this_option['text'].split())
					value = variables.set(this_option['input']['var'], value)
					# with open('out.txt', 'a') as fp:
					# 	fp.write(str(value) + '\n')
					break

				if 'return' in this_option and this_option['return']:
					menus = menus[:-1]
					if not len(menus): break
				elif 'goto' in this_option:
					menus += [this_option['goto']]
			except display.CancelInput:
				menus = menus[:-1]
				if not len(menus): break

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
