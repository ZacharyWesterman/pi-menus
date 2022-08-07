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
		current_index = 0

		menu_stack = []

		while True:
			#If we hit an invalid menu, show the error, then go back
			try:
				menu_item = self.get_menu_config(current_menu)
			except UnknownMenu as e:
				await self.display.message(str(e), title='Unhandled Exception')
				await asyncio.sleep(2)
				if len(menu_stack):
					current_menu, current_index = menu_stack.pop(-1)
					continue
				else:
					break #If user exited the last menu, return

			try:
				if menu_item['type'] == 'menu':
					selection = await self.display.menu(menu_item, current_index)
					#get a value and set a var based on that
					if 'input' in selection:
						cfg = selection['input']
						if type(cfg) is not dict:
							raise BadConfig(cfg)

						is_password = cfg.get('password', False)
						value = await self.display.get(is_password)
						await self.display.message(title='Loading...', subtitle='Please be patient.')

						var_name = cfg.get('var', '')
						if var_name == '':
							raise BadVarName(var_name)

						await self.variables.set(var_name, value)

					#run specific actions based on the selection
					if 'action' in selection:
						await self.display.message(title='Processing...', subtitle='Please be patient.')
						await self.variables.action(selection['action'], display=self.display)

					#move to a new menu
					if 'goto' in selection:
						menu_stack.append((current_menu, self.display.menu_position()))
						current_menu = selection['goto']

					if selection.get('return', False):
						raise display.CancelInput

				elif menu_item['type'] == 'message':
					await self.display.message(text='Please be patient.', title='Loading...')

					title = await self.variables.parse(menu_item.get('title', ''))
					subtitle = await self.variables.parse(menu_item.get('subtitle', ''))
					text = await self.variables.parse(menu_item.get('text', ''))
					await self.display.message(text=text, title=title, subtitle=subtitle)

					await self.display.await_movement()
					raise display.CancelInput

			except display.CancelInput:
				if len(menu_stack):
					current_menu, current_index = menu_stack.pop(-1)
				else:
					break #If user exited the last menu, return
			except Exception as e:
				await self.display.message(str(e), title='Unhandled Exception')
				await asyncio.sleep(2)

		#do any cleanup here
