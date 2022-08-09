#!/usr/bin/env python3
import menu
import asyncio
from pathlib import Path
import os

if __name__ == '__main__':
	os.chdir(str(Path(__file__).parent)) #Make sure working dir is always in the project root
	manager = menu.Manager()
	try:
		asyncio.run(manager.run())
	except KeyboardInterrupt:
		pass
	finally:
		manager.cleanup()
