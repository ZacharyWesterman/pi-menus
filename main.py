#!/usr/bin/env python3
import menu_manager
import asyncio

async def main():
	manager = menu_manager.Manager()
	await manager.run()

if __name__ == '__main__':
	asyncio.run(main())
