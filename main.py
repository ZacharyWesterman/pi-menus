#!/usr/bin/env python3
import menu
import asyncio
from pathlib import Path
import os
from sys import argv

def main():
	manager = menu.Manager()
	try:
		asyncio.run(manager.run())
	except KeyboardInterrupt:
		manager.cleanup()
		return False

	manager.cleanup()
	return True

if __name__ == '__main__':
	os.chdir(str(Path(__file__).parent)) #Make sure working dir is always in the project root
	looping = True if '--loop' in argv else False

	if '--loop' in argv:
		while main():
			pass
	else:
		main()
