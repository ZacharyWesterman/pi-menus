from behaviors import register

import asyncio
import time

@register('shutdown')
async def shutdown_action(display: object, **args) -> None:
	await display.message(title='Shutting down...')
	process = await asyncio.create_subprocess_shell(
		'shutdown now',
		shell = True,
		stdout = asyncio.subprocess.PIPE,
		stderr = asyncio.subprocess.PIPE
	)
	stdout, stderr = await process.communicate()

	time.sleep(20) #we WANT this to be blocking
