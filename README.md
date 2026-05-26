# MACSWAP

Вообще делал для себя, но может кому-то нужно.
Не помню че там и как я делал(уже не использую), но вот чета написал блин

MAC address changer for Arch Linux.

Install:

sudo pacman -S python macchanger iproute2

Run:

sudo python3 macswap.py

Random MAC:

sudo python3 macswap.py wlan0 -r

Same Vendor MAC:

sudo python3 macswap.py wlan0 -e

Custom MAC:

sudo python3 macswap.py wlan0 -m 00:11:22:33:44:55

Auto Mode:

sudo python3 macswap.py wlan0 -r -t 5m

Dry Run:

python3 macswap.py --dry-run

Help:

python3 macswap.py --help

License: MIT
