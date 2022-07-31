from enum import Enum
import abc

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

	@abc.abstractmethod
	def display(self) -> None:
		pass

	@abc.abstractmethod
	def clear(self) -> None:
		pass

	@abc.abstractmethod
	def get(self, hidden: bool = False) -> str:
		pass

	@abc.abstractmethod
	def put(self, row: int, text: str, *, bold: bool = False, italics: bool = False, inverted: bool = False, is_option: bool = False) -> None:
		pass

	@abc.abstractmethod
	def await_movement(self) -> None:
		pass

	# Below this comment, no more methods need to be implemented by child classes.

	def __print_menu(self, options: list, title: str, subtitle: str) -> None:
		offset = 0

		if len(title):
			self.put(offset, title, bold = True)
			offset += 1
		if len(subtitle):
			self.put(offset, subtitle, italics = True)
			offset += 1

		for i in range(0, len(options)):
			if i == self.menu_index:
				text = options[i]['alt'] if 'alt' in options[i] else options[i]['text']
				self.put(i+offset, text, inverted = True, is_option = True)
			else:
				text = options[i]['text']
				self.put(i+offset, text, is_option = True)

		self.display()

	def message(self, text: str, title: str = '') -> None:
		self.clear()
		if len(title):
			self.put(0, title, bold = True)
			self.put(1, text)
		else:
			self.put(0, text)
		self.display()

	def menu_move_down(self) -> None:
		if self.menu_index < (self.menu_max_options - 1):
			self.menu_index += 1
			self.redisplay_menu()

	def menu_move_up(self) -> None:
		if self.menu_index > 0:
			self.menu_index -= 1
			self.redisplay_menu()

	def menu(self, menu_item: dict) -> dict:
		title = self.variables.parse(menu_item['title']) if 'title' in menu_item else ''
		subtitle = self.variables.parse(menu_item['subtitle']) if 'subtitle' in menu_item else ''
		options = self.__build_options(menu_item)

		self.menu_index = 0
		self.menu_max_options = len(options)
		self.redisplay_menu = lambda: self.__print_menu(options, title, subtitle)
		self.scroll_up = self.menu_move_up
		self.scroll_down = self.menu_move_down

		try:
			while True:
				self.__print_menu(options, title, subtitle)
				self.await_movement()

				#if this option does anything, we selected it
				if any(k in options[self.menu_index] for k in ('input', 'action', 'return', 'goto')):
					break

			self.clear()
			return options[index]

		except CancelInput:
			self.clear()
			raise CancelInput

	def __build_options(self, menu_item: dict) -> list:
		options = []

		for option in menu_item['options']:
			options += [self.__parse_menu_option(option)]

		# If there's a template (for dynamic lists), build it and add to options
		if 'template' in menu_item:
			var = menu_item['template']['var']
			value = self.variables.get(var)
			self.variables.set(var, value)
			for line in value.split('\n'):
				self.variables.set('line', line)
				items = line.split()
				items += [''] * (10 - len(items))
				self.variables.set('item', items)
				for option in menu_item['template']['options']:
					options += [self.__parse_menu_option(option)]

		return options

	def __parse_menu_option(self, option: dict) -> dict:
		new_opt = {}
		for i in option:
			if type(option[i]) is str:
				new_opt[i] = self.variables.parse(option[i])
			elif type(option[i]) is dict:
				new_opt[i] = self.__parse_menu_option(option[i])
			else:
				new_opt[i] = option[i]

		return new_opt
