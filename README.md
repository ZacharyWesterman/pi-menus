# pi-menus
quick and simple menu interface for multiple kinds of display/input devices

Requirements:
* sudo apt install nmap network-manager
* pip3 install pillow smbus numpy==1.21.3 spidev RPi.GPIO

Note that numpy **must be version 1.21.3**! In version 1.21.5 (on the Pi Zero W), running `import numpy` gives an `Illegal Instruction` crash message.
