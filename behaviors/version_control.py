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

		return stdout.decode().rstrip('\n')

	def get_version():
		with open('config/version.txt', 'r') as fp:
			return fp.read().strip()

	#Check if update is available
	await run_cmd('git fetch')
	updated_files = await run_cmd('git log --name-status origin/main..')

	#If no updates available, exit
	if updated_files == '':
		await display.message('Already up-to-date.')
		await asyncio.sleep(2)
		return

	await display.message(title='Update Available', text='Installing Update...')

	old_version = get_version()
	await run_cmd('git pull --ff-only --quiet')
	await run_cmd('chown pi:pi .git * -R')
	new_version = get_version()

	#ALWAYS make sure python dependencies are installed.
	await run_cmd('venv/bin/python -m pip install -r requirements.txt --no-warn-script-location')

	await display.message(title='Version Updated', subtitle=f'{old_version} to {new_version}', text='Please exit main menu \nto finish update.')
	await display.user_acknowledge()
