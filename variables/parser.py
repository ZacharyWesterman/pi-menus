#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import asyncio

class FailedVarLoad(Exception):
	def __init__(self, var_name: str):
		super().__init__(f'Failed to get usable output from "{var_name}"')

class UnknownAction(Exception):
	def __init__(self, var_name: str):
		super().__init__(f'Action "{var_name}" is undefined')

class Parser:
	def __init__(self, filename: str = ''):
		self.__config = {}
		self.__vars = {}
		if len(filename):
			self.load(filename)

	async def __get_output_of(self, command: str): #could return anything
		if isinstance(command, dict):
			if 'bash' in command:
				result = await self.__run_bash_cmd(command['bash'])
				if result == '':
					raise FailedVarLoad(command['bash'])
				delim = command.get('delim')

				return result if delim is None else result.split(delim)
			else:
				raise FailedVarLoad(command)
		else:
			raise FailedVarLoad(command)

	async def __run_bash_cmd(self, command: str) -> str:
		process = await asyncio.create_subprocess_shell(
			command,
			shell = True,
			stdout = asyncio.subprocess.PIPE,
			stderr = asyncio.subprocess.PIPE
		)
		stdout, stderr = await process.communicate()
		return stdout.decode('utf-8').rstrip('\n')

	def load(self, filename: str) -> None:
		with open(filename, 'r') as fp:
			self.__config = json.load(fp)

	def clear(self) -> None:
		self.__config = {}
		self.__vars = {}

	def set_config(self, var_name: str, var_config: dict) -> None:
		self.__config[var_name] = var_config

	def del_config(self, var_name: str) -> None:
		if var_name in self.__config:
			del self.__config[var_name]

	def unset(self, var_name: str) -> None:
		self.__vars.pop(var_name, None)

	async def set(self, var_name: str, var_value: str) -> None:
		self.__vars[var_name] = var_value
		if var_name in self.__config:
			# If this var has logic that happens when it gets set, run that.
			if 'unset' in self.__config[var_name]:
				unset_list = self.__config[var_name]['unset']
				if type(unset_list) is str:
					unset_list = [unset_list]
				for var in unset_list:
					self.unset(var)

			if 'set' in self.__config[var_name]:
				setcmd = self.__config[var_name]['set']
				if isinstance(setcmd, dict):
					if 'bash' in setcmd:
						result = await self.__get_output_of(setcmd['bash'])
					else:
						raise FailedVarLoad(setcmd)
				else:
					raise FailedVarLoad(setcmd)

	async def get(self, var_name: str): #This could return anything!
		#Don't keep any vars that are not cached!
		if (var_name in self.__vars) and (var_name in self.__config) and self.__config[var_name].get('cache', False):
			self.unset(var_name)

		if var_name not in self.__vars:
			if var_name not in self.__config:
				return '{?' + var_name + '?}' #var not in config, so can't load it.
			elif 'get' in self.__config[var_name]:
				try:
					result = await self.__get_output_of(self.__config[var_name]['get'])
					await self.set(var_name, result)
					return result
				except FailedVarLoad:
					return '{!' + var_name + '!}'
			else:
				return '{' + var_name + '}'
		else:
			return self.__vars[var_name]

	async def action(self, var_name: str) -> None:
		if var_name in self.__config and 'action' in self.__config[var_name]:
			await self.__get_output_of(self.__config[var_name]['action'])
		else:
			raise UnknownAction(var_name)

	async def parse(self, text: str) -> str:
		try:
			return text.format(**self.__vars)
		except KeyError as ex:
			failed_vars = self.__vars
			for var_name in ex.args:
				failed_vars[var_name] = await self.get(var_name)

			return text.format(**failed_vars)
