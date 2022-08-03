#!/usr/bin/env python3
import menu_manager
import asyncio
import traceback

async def main():
	manager = menu_manager.Manager()
	await manager.run()


if __name__ == '__main__':
	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	loop.run_until_complete(main())
	loop.close()
