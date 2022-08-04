from .interface import CancelInput

try:
	from .oled_display import Display
except ModuleNotFoundError:
	from .term_display import Display
