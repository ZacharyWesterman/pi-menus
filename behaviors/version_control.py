from behaviors import register

import asyncio

@register('fetch_update')
async def fetch_update(variables: object) -> None:
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
			raise Exception(f'Failed to fetch update:\n{stderr}')

	await run_cmd('git pull')
	await run_cmd('chown pi:pi .git * -R')
