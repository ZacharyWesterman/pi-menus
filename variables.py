#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import asyncio

with open('vars.json', 'r') as fp:
	__vars_config = json.load(fp)

__variables = {}

async def parse(text: str) -> str:
	global __variables
	global __vars_config

	try:
		return text.format(**__variables)
	except KeyError as ex:
		for key in ex.args:
			__variables[key] = await get(key)

		result = text.format(**__variables)

		for key in ex.args:
			if key in __variables and key in __vars_config and 'cache' in __vars_config[key] and not __vars_config[key]['cache']:
				unset(key)

		return result

async def get(key: str):
	global __variables
	global __vars_config

	if key in __variables and key in __vars_config and 'cache' in __vars_config[key] and not __vars_config[key]['cache']:
		unset(key)

	if key not in __variables:
		if key not in __vars_config:
			return '{' + key + '}' #will be wrong value, but should be obvious when displayed
		elif 'get' in __vars_config[key]:
			try:
				process = await asyncio.create_subprocess_shell(
					__vars_config[key]['get'],
					shell = True,
					stdout = asyncio.subprocess.PIPE,
					stderr = asyncio.subprocess.PIPE
				)
				stdout, stderr = await process.communicate()

				return stdout.decode('utf-8').rstrip('\n')
			except Exception as e:
				print(e)
				return '{!' + key + '!}'
		else:
			return '{' + key + '}'
	else:
		return __variables[key]

def set(key: str, value: str) -> None:
	global __variables
	__variables[key] = value
	if key in __vars_config:
		if 'set' in __vars_config[key]:
			cmd = parse(__vars_config[key]['set'])
			try:
				subprocess.check_output(cmd, shell=True)
			except:
				pass
		if 'unset' in __vars_config[key]:
			for i in __vars_config[key]['unset']:
				unset(i)

def unset(key: str) -> None:
	global __variables
	__variables.pop(key, None)
