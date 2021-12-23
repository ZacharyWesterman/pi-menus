#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import oled_display as display
import json
import time
import variables
import subprocess

if __name__ == '__main__':
	try:
		USER_SHUTDOWN = False

		display.start()

		with open('menu.json', 'r') as fp:
			menu_display = json.load(fp)

		menus = ['main']

		while True:
			this_menu = menu_display[menus[-1]]
			try:
				display.message('Loading...')
				this_option = display.menu(this_menu)

				if 'input' in this_option:
					value = display.get('password' in this_option['input'] and this_option['input']['password'])
					variables.set('line', this_option['text'])
					items = this_option['text'].split()
					items += [''] * (10 - len(items))
					variables.set('item', items)
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
				#if we're at the root menu and user exits
				if len(menus) == 1:
					#Prompt user if they want to shut down
					shutdown_menu = {
						'options': [
							{
								'text': 'Shut Down',
								'return': True
							},
							{
								'text': 'Reset',
								'return': True
							},
							{
								'text': 'Cancel',
								'return': True
							}
						]
					}

					try:
						this_option = display.menu(shutdown_menu)
						if this_option['text'] == 'Shut Down':
							USER_SHUTDOWN = True
							break
						elif this_option['text'] == 'Reset':
							break
					except display.CancelInput:
						pass
				else:
					#go to parent menu
					menus = menus[:-1]

			time.sleep(0.1)

			# print(menus)

		if USER_SHUTDOWN:
			#User signalled shutdown
			display.message('Shutting down...')
			try:
				subprocess.check_output(['shutdown', 'now'])
			except:
				pass
		exit()

	except KeyboardInterrupt:
		display.stop()
		print("User signalled interrupt. Exiting.")
		exit()

	except Exception as e:
		display.stop()
		raise e
