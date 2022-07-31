#!/usr/bin/env python3

import time
import display
import variables

disp = display.Display(variables)

try:
	selected = disp.menu({
		'title': 'sample menu',
		'options': [
			{ 'text': 'sample text' },
			{ 'text': 'text 2' },
		]
	})

	disp.clear()

	print(selected)
except display.CancelInput:
	pass

time.sleep(2)
