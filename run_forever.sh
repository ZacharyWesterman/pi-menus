#!/usr/bin/env bash

#Run the main menu script forever.
#This way, if the program crashes or user restarts it,
#they don't have to reboot the whole thing.

cd "$(dirname ${BASH_SOURCE[0]})"

while [ ! -e CMD_STOP ]
do
	./main.py
done
