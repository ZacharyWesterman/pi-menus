#!/usr/bin/env python3

import display
import variables
import asyncio


async def main():
	disp = display.Display(variables)
	try:
		selected = await disp.menu({
			'title': 'sample menu',
			# 'subtitle': 'some extra descriptive text',
			'options': [
				{ 'text': f'option {i}' } for i in range(1,10)
			]
		})
	except Exception as e:
		disp.message(str(e), title='ERROR', subtitle='Unhandled Exception')
		await asyncio.sleep(2)


if __name__ == '__main__':
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	loop.run_until_complete(main())
	loop.close()
# time.sleep(2)
