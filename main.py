#!/usr/bin/env python3
import menu
import asyncio
import signal
from pathlib import Path
import os
from sys import argv, executable

class GracefulExit(SystemExit):
	pass

def graceful_terminate(manager):
	manager.cleanup()
	raise GracefulExit()

async def main():
	manager = menu.Manager()

	loop = asyncio.get_event_loop()
	loop.add_signal_handler(signal.SIGTERM, graceful_terminate, manager)
	loop.add_signal_handler(signal.SIGABRT, graceful_terminate, manager)
	loop.add_signal_handler(signal.SIGINT, graceful_terminate, manager)

	await manager.run()

if __name__ == '__main__':
	os.chdir(str(Path(__file__).parent)) #Make sure working dir is always in the project root

	if '--loop' in argv:
		while True:
			asyncio.run(main())
			#If user exits, reload this whole program
			os.execl(executable, executable, *argv)
	else:
		asyncio.run(main())
