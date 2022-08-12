from behaviors import register

import asyncio

@register('fetch_update')
async def fetch_update(variables: object, display: object, **args) -> None:
	async def run_cmd(cmd: str):
		process = await asyncio.create_subprocess_shell(
			cmd,
			shell = True,
			stdout = asyncio.subprocess.PIPE,
			stderr = asyncio.subprocess.PIPE
		)
		stdout, stderr = await process.communicate()

		if len(stderr):
			stderr = stderr.decode().rstrip('\n')
			print(stderr)
			raise Exception(f'Failed to fetch update:\n{stderr}')

	def get_version():
		with open('config/version.txt', 'r') as fp:
			return fp.read().strip()

	old_version = get_version()
	await run_cmd('git pull --ff-only --quiet')
	await run_cmd('chown pi:pi .git * -R')
	new_version = get_version()

	if old_version != new_version:
		await display.message(title='Version Updated', subtitle=f'{old_version} to {new_version}', text='Please exit main menu \nto finish update.')
		await display.user_acknowledge()
