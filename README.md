### Pi-Menus

This package lets you turn your Raspberry Pi into a small network analysis toolkit.

It's intended for the rPi zero W running the latest [Raspberry Pi OS Lite (32-bit)](https://www.raspberrypi.com/software/operating-systems/), but it should work on other models / versions.

Before installing:
* Make sure the Pi's SPI and wireless interfaces are enabled.
* Note that the default display interface is the [Waveshare 1.3inch OLED HAT](https://www.waveshare.com/1.3inch-oled-hat.htm). That and CLI are the only supported interfaces currently.
* Note that, since this program manages network access for the Pi, it runs as root. If that's an issue, you can disable the daemon and run manually as a normal user. Some functionality may not work in that case.

---

### Getting Started

To install, run `./install.sh`. This will install all dependencies and start the service daemon.

If you want to run via command line, first stop the service
```bash
sudo systemctl stop pi-menus
```
Then run the program manually. You may omit the `sudo` if you don't need full access to network tools.
```bash
sudo venv/bin/python main.py --term
```

Note that `main.py` requires you to specify which user interface is used. If no interface is specified, the program will spit out an error message and immediately exit.

| Flag     | Meaning                            |
| -------- | ---------------------------------- |
| `--term` | Use the terminal as user interface |
| `--oled` | Use the OLED HAT as user interface |
| `--loop` | Restart the program on exit        |
