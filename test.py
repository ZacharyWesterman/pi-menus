#!/usr/bin/env python3

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
					}
				]
			},
		})
	except display.CancelInput:
		pass #User cancelled
	except Exception as e:
		disp.message(str(e), title='ERROR', subtitle='Unhandled Exception')
		await asyncio.sleep(2)


if __name__ == '__main__':
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	loop.run_until_complete(main())
	loop.close()
# time.sleep(2)
