#!/usr/bin/env bash

fail() {
	echo 'ERROR: Failed to complete installation. See error messages above.'
	exit 1
}

sudo apt install nmap libopenjp2-7 libatlas-base-dev python3-venv -y || fail
python -m venv venv || fail
source venv/bin/activate || fail
python -m pip install -r config/requirements.txt || fail
