#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import subprocess

with open('vars.json', 'r') as fp:
	__vars_config = json.load(fp)

__variables = {}

def parse(text: str) -> str:
	global __variables

	try:
		return text.format(**__variables)
	except KeyError as ex:
		for key in ex.args:
			__variables[key] = get(key)

		return text.format(**__variables)

def get(key: str):
	global __variables
	global __vars_config

	if key not in __variables:
		if key not in __vars_config:
			return '{' + key + '}' #will be wrong value, but should be obvious when displayed
		elif 'bash' in __vars_config[key]:
			return subprocess.check_output(__vars_config[key]['bash'], shell=True).decode('utf-8').rstrip('\n')
		else:
			return '{' + key + '}'
	else:
		return __variables[key]

def set(key: str, value: str) -> None:
	global __variables
	__variables[key] = value

def unset(key: str) -> None:
	global __variables
	__variables.pop(key, None)
