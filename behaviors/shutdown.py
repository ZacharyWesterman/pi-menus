from behaviors import register

import asyncio

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

	await asyncio.sleep(20) #Don't display anything else

@register('reboot')
async def reboot_action(display: object, **args) -> None:
	await display.message(title='Restarting...')
	process = await asyncio.create_subprocess_shell(
		'shutdown -r now',
		shell = True,
		stdout = asyncio.subprocess.PIPE,
		stderr = asyncio.subprocess.PIPE
	)
	stdout, stderr = await process.communicate()

	await asyncio.sleep(20) #Don't display anything else
