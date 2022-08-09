#!/usr/bin/env bash

#Run the main menu script forever.
#This way, if the program crashes or user restarts it,
#they don't have to reboot the whole thing.

terminate() {
	kill $process_id
}

trap terminate SIGINT SIGTERM

cd "$(dirname ${BASH_SOURCE[0]})"

while true
do
	venv/bin/python main.py --oled &
	process_id=$!
	wait
done
