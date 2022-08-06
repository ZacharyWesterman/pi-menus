from behaviors import register

import asyncio

@register('shutdown')
async def shutdown_action(display: object, **args) -> None:
	display.message(title='Shutting down...')
	process = await asyncio.create_subprocess_shell(
		'shutdown now',
		shell = True,
		stdout = asyncio.subprocess.PIPE,
		stderr = asyncio.subprocess.PIPE
	)
	stdout, stderr = await process.communicate()
