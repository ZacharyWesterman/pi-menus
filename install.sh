#!/usr/bin/env bash

cd "$(dirname "${BASH_SOURCE[0]}")" || exit 1

fail() {
	echo 'ERROR: Failed to complete installation. See error messages above.'
	exit 1
}

sudo apt install nmap libopenjp2-7 libatlas-base-dev python3-venv -y || fail
python -m venv venv || fail
source venv/bin/activate || fail
python -m pip install -r config/requirements.txt || fail

echo "[Unit]
Description=Service to run OLED menus on startup

[Service]
ExecStart=$(pwd)/venv/bin/python $(pwd)/main.py --oled --loop

[Install]
WantedBy=multi-user.target" > tmp
sudo mv tmp /etc/systemd/system/pi-menus.service
sudo systemctl daemon-reload
sudo systemctl enable pi-menus
sudo systemctl start pi-menus
