import json
import asyncio

from .exceptions import *
import behaviors

class Parser:
	def __init__(self):
		self.__config = {}
		self.__vars = {}
		self.display = None
		self.load('config/vars.json')

	async def __get_output_of(self, command: str, *, allow_null: bool = False): #could return anything
		if isinstance(command, dict):
			if 'bash' in command:
				cmd = await self.parse(command['bash'])
				result = await self.__run_bash_cmd(cmd)
				if result == '' and not allow_null:
					raise FailedVarLoad(cmd)
				delim = command.get('delim')

				return result if delim is None else result.split(delim)
			elif 'py' in command:
				behavior = behaviors.get(command['py'])
				return await behavior(variables=self, display=self.display)
		else:
			behavior = behaviors.get(command)
			return await behavior(variables=self)

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
				result = await self.__get_output_of(setcmd, allow_null=True)

	async def get(self, var_name: str): #This could return anything!
		if var_name not in self.__vars:
			if var_name not in self.__config:
				raise UnknownVar(var_name) #var not in config, so can't load it.
			elif 'get' in self.__config[var_name]:
				result = await self.__get_output_of(self.__config[var_name]['get'], allow_null=True)
				await self.set(var_name, result)
				print(f'set {var_name} to {result}')
				if not self.__config[var_name].get('cache', True):
					self.unset(var_name)
				return result
			elif 'default' in self.__config[var_name]:
				default = self.__config[var_name]['default']
				await self.set(var_name, default)
				return default
			else:
				raise CannotLoadVar(var_name)
		else:
			return self.__vars[var_name]

	async def action(self, var_name: str) -> None:
		if var_name in self.__config and 'action' in self.__config[var_name]:
			await self.__get_output_of(self.__config[var_name]['action'], allow_null=True)
		else:
			raise UnknownAction(var_name)

	async def parse(self, text: str) -> str:
		failed_vars = {}

		for i in range(20): #DON'T loop forever!
			try:
				return text.format(**self.__vars, **failed_vars)
			except KeyError as ex:
				for var_name in ex.args:
					result = await self.get(var_name)
					if var_name not in self.__vars:
						failed_vars[var_name] = result
