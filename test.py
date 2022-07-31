#!/usr/bin/env python3.7

import display
import variables
import asyncio


async def main():
	disp = display.Display(variables)
	try:
		selected = await disp.menu({
			'title': 'Software Version',
			'subtitle': '{software_version}',
			"template": {
				"var": "test_list",
				"options": [
					{
						"text": "{line}",
						"input": "software_version"
					}
				]
			},
		})

		input = await disp.get()
		disp.message(input, title='Result')
		await asyncio.sleep(2)
	except display.CancelInput:
		pass #User cancelled
	except Exception as e:
		# disp.message(str(e), title='ERROR', subtitle='Unhandled Exception')
		print(e)
		await asyncio.sleep(2)


if __name__ == '__main__':
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	loop.run_until_complete(main())
	loop.close()
