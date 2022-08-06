class FailedVarLoad(Exception):
	def __init__(self, var_name: str):
		super().__init__(f'Failed to get usable output from "{var_name}"')

class UnknownAction(Exception):
	def __init__(self, var_name: str):
		super().__init__(f'Action "{var_name}" is undefined')
