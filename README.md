# pi-menus
quick and simple menu interface for multiple kinds of display/input devices

Requirements:
* sudo apt install nmap network-manager
* sudo pip3 install luma.oled pillow smbus
* sudo pip3 install numpy==1.21.3

Note that numpy **must be version 1.21.3**! Version 1.21.5 (on the Pi Zero W) `import numpy` gives an `Illegal Instruction` crash message.
