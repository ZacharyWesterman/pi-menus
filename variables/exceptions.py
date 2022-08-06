class FailedVarLoad(Exception):
	def __init__(self, var_name: str):
		super().__init__(f'No usable result for "{var_name}".')

class UnknownVar(Exception):
	def __init__(self, var_name: str):
		super().__init__(f'Var "{var_name}" definition not found.')

class CannotLoadVar(Exception):
	def __init__(self, var_name: str):
		super().__init__(f'Var "{var_name}" has no get action or default value.')

class UnknownAction(Exception):
	def __init__(self, var_name: str):
		super().__init__(f'Action "{var_name}" is undefined.')
