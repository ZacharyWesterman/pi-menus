__all__ = ['register', 'all', 'get', 'UnknownBehavior']

__behav_list = {}

class UnknownBehavior(Exception):
	def __init__(self, name: str):
		super().__init__(f'Behavior "{name}" not registered.')

def register(name: str) -> callable:
	def inner(method: callable) -> callable:
		global __behav_list
		__behav_list[name] = method
		return method

	return inner

def all() -> dict:
	global __behav_list
	return __behav_list

def get(name: str, default = None) -> callable:
	global __behav_list
	if name in __behav_list:
		return __behav_list[name]
	else:
		raise UnknownBehavior(name)

#Dynamically import and register all behaviors
import glob
from pathlib import Path
this = Path(__file__)
importlist = [ i.name[:-3] for i in this.parent.iterdir() if i.name != '__init__.py' and i.is_dir() == False ]

for i in importlist:
	__import__(f'behaviors.{i}')
