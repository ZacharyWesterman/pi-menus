class NoEntryPoint(Exception):
	def __init__(self):
		super().__init__('No "main" entry point in menu config!')

class BadMenuReference(Exception):
	def __init__(self, name: str):
		super().__init__(f'Unknown menu item "{name}"')

class BadVarName(Exception):
	def __init__(self, name: str):
		super().__init__(f'Invalid var name "{name}"')

class UnknownMenu(Exception):
	def __init__(self, name: str):
		super().__init__(f'Unknown menu "{name}"')

class BadConfig(Exception):
	def __init__(self, config_item):
		super().__init__(f'Bad config {config_item}')
