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
			{ 'text': f'option {i}' } for i in range(1,100)
		]
	})

	print(selected)
except display.CancelInput:
	print('User Cancelled')
except Exception as e:
	print(e)

time.sleep(2)
