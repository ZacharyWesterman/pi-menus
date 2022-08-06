from .exceptions import CancelInput

from sys import argv

if '--oled' in argv:
	from .oled_display import Display
elif '--term' in argv:
	from .term_display import Display
else:
	print('ERROR: No display specified. Run with either --term or --oled.')
	exit(1)
