#!/usr/bin/env python3
import menu
import asyncio
from pathlib import Path
import os

async def main():
	manager = menu.Manager()
	try:
		await manager.run()
	except KeyboardInterrupt:
		pass #exit gracefully

if __name__ == '__main__':
	os.chdir(str(Path(__file__).parent)) #Make sure working dir is always in the project root
	asyncio.run(main())
