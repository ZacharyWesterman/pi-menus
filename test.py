#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import display
import json
import time

if __name__ == '__main__':
	try:
		display.start()

		with open('menu.json', 'r') as fp:
			main_menu = json.load(fp)

		# display.put('input: ', 0, 0)
		# result = display.get()
		result = display.menu(main_menu, 'Example menu')
		display.clear()
		display.put(f'result={result}', 0, 1)

		time.sleep(1)
		display.stop()

	except KeyboardInterrupt:
		display.stop()
		print("User signalled interrupt. Exiting.")
		exit()

	except Exception as e:
		display.stop()
		raise e
