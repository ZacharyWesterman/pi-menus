#!/usr/bin/env python3
import menu
import asyncio

async def main():
	manager = menu.Manager()
	await manager.run()

if __name__ == '__main__':
	asyncio.run(main())
