import asyncio
import json
import traceback

import display
import variables

from .exceptions import *

class Manager():
	def __init__(self):
		with open('config/menu.json', 'r') as fp:
			self.menu_config = json.load(fp)

		if 'main' not in self.menu_config:
			raise NoEntryPoint()

		self.variables = variables.Parser()
		self.display = display.Display(self.variables)

	def get_menu_config(self, name: str) -> dict:
		if name in self.menu_config:
			return self.menu_config[name]
		else:
			raise UnknownMenu(name)

	async def run(self) -> None:
		current_menu = 'main'

		menu_stack = []

		while True:
			#If we hit an invalid menu, show the error, then go back
			try:
				menu_item = self.get_menu_config(current_menu)
			except UnknownMenu as e:
				self.display.message(str(e), title='Unhandled Exception')
				await asyncio.sleep(2)
				if len(menu_stack):
					current_menu = menu_stack.pop(-1)
					continue
				else:
					break #If user exited the last menu, return

			try:
				selection = await self.display.menu(menu_item)
				#get a value and set a var based on that
				if 'input' in selection:
					cfg = selection['input']
					if type(cfg) is not dict:
						raise BadConfig(cfg)

					is_password = cfg.get('password', False)
					value = await self.display.get(is_password)
					self.display.message(title='Loading...', subtitle='Please be patient.')

					var_name = cfg.get('var', '')
					if var_name == '':
						raise BadVarName(var_name)

					await self.variables.set(var_name, value)

				#run specific actions based on the selection
				if 'action' in selection:
					self.display.message(title='Processing...', subtitle='Please be patient.')
					await self.variables.action(selection['action'])

				#move to a new menu
				if 'goto' in selection:
					menu_stack.append(current_menu)
					current_menu = selection['goto']

				if selection.get('return', False):
					raise display.CancelInput

			except display.CancelInput:
				if len(menu_stack):
					current_menu = menu_stack.pop(-1)
				else:
					break #If user exited the last menu, return
			except Exception as e:
				self.display.message(str(e), title='Unhandled Exception')
				await asyncio.sleep(2)

		#do any cleanup here
