import RPi.GPIO as GPIO

#GPIO define
RST        = 25
CS         = 8
DC         = 24

KEY_UP     = 6
KEY_DOWN   = 19
KEY_LEFT   = 5
KEY_RIGHT  = 26
KEY_PRESS  = 13

KEY1       = 21
KEY2       = 20
KEY3       = 16

def init():
	#init GPIO
	# for P4:
	# sudo vi /boot/config.txt
	# gpio=6,19,5,26,13,21,20,16=pu
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(KEY_UP,      GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
	GPIO.setup(KEY_DOWN,    GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
	GPIO.setup(KEY_LEFT,    GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
	GPIO.setup(KEY_RIGHT,   GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
	GPIO.setup(KEY_PRESS,   GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
	GPIO.setup(KEY1,        GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
	GPIO.setup(KEY2,        GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
	GPIO.setup(KEY3,        GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
