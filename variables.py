#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import subprocess

with open('vars.json', 'r') as fp:
	__vars_config = json.load(fp)

__variables = {}

def parse(text: str) -> str:
	global __variables
	global __vars_config

	try:
		return text.format(**__variables)
	except KeyError as ex:
		for key in ex.args:
			__variables[key] = get(key)

		result = text.format(**__variables)

		for key in ex.args:
			if key in __variables and key in __vars_config and 'cache' in __vars_config[key] and not __vars_config[key]['cache']:
				unset(key)

		return result

def get(key: str):
	global __variables
	global __vars_config

	if key not in __variables:
		if key not in __vars_config:
			return '{' + key + '}' #will be wrong value, but should be obvious when displayed
		elif 'get' in __vars_config[key]:
			return subprocess.check_output(__vars_config[key]['get'], shell=True).decode('utf-8').rstrip('\n')
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
			subprocess.check_output(cmd, shell=True)
		if 'unset' in __vars_config[key]:
			for i in __vars_config[key]['unset']:
				unset(i)

def unset(key: str) -> None:
	global __variables
	__variables.pop(key, None)
