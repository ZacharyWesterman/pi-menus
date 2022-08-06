class CancelInput(Exception):
	def __init__(self):
		super().__init__('Unhandled user-input "cancel" action.')

class NotImplemented(Exception):
	def __init__(self, method):
		super().__init__(f'{method.__name__} is not implemented.')
