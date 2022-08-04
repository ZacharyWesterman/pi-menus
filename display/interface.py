from enum import Enum
import abc
import asyncio
import copy

class message(Enum):
	text = 1
	password = 2

class CancelInput(Exception):
	def __init__(self):
		super().__init__('Unhandled user-input "cancel" action.')

class NotImplemented(Exception):
	def __init__(self, method):
		super().__init__(f'{method.__name__} is not implemented.')

class DisplayInterface(metaclass=abc.ABCMeta):
	def __init__(self, variable_handler: object):
		self.variables = variable_handler
		self.menu_index = 0
		self.menu_max_options = 0

	# The following methods MUST be implemented by child classes!

	@abc.abstractmethod
	def max_height(self) -> int:
		pass

	@abc.abstractmethod
	def max_width(self) -> int:
		pass

	@abc.abstractmethod
	def text_scale(self) -> int:
		pass

	@abc.abstractmethod
	def line_scale(self) -> int:
		pass

	@abc.abstractmethod
	def display(self) -> None:
		pass

	@abc.abstractmethod
	def clear(self) -> None:
		pass

	@abc.abstractmethod
	async def get(self, hidden: bool = False) -> str:
		pass

	@abc.abstractmethod
	def put(self, y_pos: int, text: str, *, bold: bool = False, italics: bool = False, inverted: bool = False, is_option: bool = False) -> None:
		pass

	@abc.abstractmethod
	def hline(self, x_pos: int, y_pos: int, width: int) -> None:
		pass

	@abc.abstractmethod
	def vline(self, x_pos: int, y_pos: int, height: int) -> None:
		pass

	@abc.abstractmethod
	def rect(self, bounds: tuple, fill: bool) -> None:
		pass

	@abc.abstractmethod
	async def await_movement(self) -> None:
		pass

	# Below this comment, no more methods need to be implemented by child classes.

	def redisplay_menu(self) -> None:
		title = self.menu_item.get('title', '')
		subtitle = self.menu_item.get('subtitle', '')
		options = self.menu_item.get('options', [])

		offset = 0
		scale = self.text_scale()

		self.clear()

		if len(title):
			self.put(offset, title, bold = True)
			offset += scale
		if len(subtitle):
			self.put(offset, subtitle, italics = True)
			offset += scale

		#draw a line to separate title from options
		self.hline(0, offset, self.max_width() - 1)
		offset += self.line_scale()

		#Only display the options we can see in the window
		max_displayable_options = (self.max_height() - offset) // scale
		total_options = len(options)
		if total_options > max_displayable_options:
			if self.menu_index >= max_displayable_options:
				end = self.menu_index + 1
				start = end - max_displayable_options
			else:
				start = 0
				end = max_displayable_options
		else:
			start = 0
			end = total_options

		index = offset
		for i in range(start, end):
			if i == self.menu_index:
				text = options[i]['alt'] if 'alt' in options[i] else options[i]['text']
				self.put(index, text, inverted = True, is_option = True)
			else:
				text = options[i]['text']
				self.put(index, text, is_option = True)

			index += scale

		if total_options > max_displayable_options:
			self.menu_scrollbar(offset, max_displayable_options)

		self.display()

	def message(self, text: str = '', *, title: str = '', subtitle: str = '') -> None:
		self.clear()
		offset = 0
		if len(title):
			self.put(offset, title, bold = True)
			offset += self.text_scale()
		if len(subtitle):
			self.put(offset, subtitle, italics = True)
			offset += self.text_scale()

		if (len(subtitle) or len(title)) and len(text):
			self.hline(0, offset, self.max_width())
			offset += self.line_scale()

		if len(text):
			self.put(offset, text)

		self.display()

	def menu_move_down(self) -> None:
		if self.menu_index < (self.menu_max_options - 1):
			self.menu_index += 1
			self.redisplay_menu()

	def menu_move_up(self) -> None:
		if self.menu_index > 0:
			self.menu_index -= 1
			self.redisplay_menu()

	async def __load_menu_vars(self) -> None:
		title = self.menu_item.get('title', '')
		subtitle = self.menu_item.get('subtitle', '')

		self.menu_item['title'], self.menu_item['subtitle'], self.menu_item['options'] = await asyncio.gather(
			self.variables.parse(title),
			self.variables.parse(subtitle),
			self.__build_options()
		)
		self.menu_max_options = len(self.menu_item.get('options', []))
		self.redisplay_menu()

	async def menu(self, menu_item: dict) -> dict:
		self.menu_item = copy.deepcopy(menu_item)
		self.menu_index = 0
		self.menu_max_options = len(self.menu_item.get('options', []))
		self.scroll_up = self.menu_move_up
		self.scroll_down = self.menu_move_down


		self.redisplay_menu()
		user_input = asyncio.create_task(self.await_movement())
		var_display = asyncio.create_task(self.__load_menu_vars())

		while True:
			if user_input.done():
				try:
					await user_input
				except Exception as e:
					var_display.cancel()
					raise e

				#if this option does anything, we selected it
				options = self.menu_item['options']
				if len(options) > self.menu_index:
					this_option = options[self.menu_index]
					if any(k in this_option for k in ('input', 'action', 'return', 'goto')):
						break

				#Otherwise, continue polling for menu navigation
				user_input = asyncio.create_task(self.await_movement())

			await asyncio.sleep(0.05)

		await var_display
		return self.menu_item['options'][self.menu_index]

	async def __build_options(self) -> list:
		options = []

		for option in self.menu_item.get('options', []):
			options += [await self.__parse_menu_option(option)]

		# If there's a template (for dynamic lists), build it and add to options
		if 'template' in self.menu_item:
			var = self.menu_item['template']['var']
			value = await self.variables.get(var)
			if type(value) is str:
				value = [value]
			for line in value:
				await self.variables.set('line', line)
				items = line.split()
				items += [''] * (10 - len(items))
				await self.variables.set('item', items)
				for option in self.menu_item['template']['options']:
					options += [await self.__parse_menu_option(option)]

		return options

	async def __parse_menu_option(self, option: dict) -> dict:
		new_opt = {}
		for i in option:
			if type(option[i]) is str:
				new_opt[i] = await self.variables.parse(option[i])
			elif type(option[i]) is dict:
				new_opt[i] = await self.__parse_menu_option(option[i])
			else:
				new_opt[i] = option[i]

		return new_opt

	def menu_scrollbar(self, offset: int, max_displayable_options: int) -> None:
		maxh = self.max_height() - 1
		maxw = self.max_width() - 1

		self.vline(maxw-2, offset, maxh)
		self.vline(maxw-1, offset, maxh)
		self.vline(maxw, offset, maxh)
