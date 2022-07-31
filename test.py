#!/usr/bin/env python3

import time
import display
import variables

disp = display.Display(variables)

try:
	selected = disp.menu({
		'title': 'sample menu',
		'subtitle': 'some extra descriptive text',
		'options': [
			{ 'text': 'sample text' },
			{ 'text': 'text 2' },
		]
	})

	print(selected)
except display.CancelInput:
	print('User Cancelled')

time.sleep(2)
