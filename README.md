# MACSWAP

Simple Linux utility for changing MAC addresses.

Supports:
- Random MAC
- Random MAC with same vendor
- Custom MAC
- Automatic MAC rotation
- Interactive menu
- CLI mode
- Dry-run mode

---

## Features

- Random MAC generation
- Vendor-preserving MAC randomization
- Custom MAC support
- Automatic rotation with timer
- Interactive terminal menu
- CLI support
- Dry-run mode
- Root permission check

---

# Requirements

- Arch Linux
- Python 3
- macchanger
- iproute2
- sudo/root

---

# Installation

Install required packages:

sudo pacman -S python macchanger iproute2

Clone project:

git clone https://github.com/yourname/macswap.git
cd macswap

Run:

sudo python3 macswap.py

---

# Interactive Menu

=== MACSWAP MENU ===

1) Random MAC
2) Random MAC (same vendor)
3) Set custom MAC
4) Auto mode
5) Exit

---

# CLI Usage

## Random MAC

sudo python3 macswap.py wlan0 -r

## Random MAC with same vendor

sudo python3 macswap.py wlan0 -e

## Set custom MAC

sudo python3 macswap.py wlan0 -m 00:11:22:33:44:55

## Auto mode

Change MAC every 5 minutes:

sudo python3 macswap.py wlan0 -r -t 5m

---

# Multiple Interfaces

sudo python3 macswap.py wlan0 eth0 -r

Auto mode on multiple interfaces:

sudo python3 macswap.py wlan0 eth0 -r -t 30s

---

# Dry Run

Show commands without executing them:

python3 macswap.py --dry-run

---

# Time Format

| Format | Description |
|--------|-------------|
| 10s | 10 seconds |
| 5m | 5 minutes |
| 1h | 1 hour |

---

# Help

python3 macswap.py --help

---

# Example Output

wlan0: 3a:92:11:ab:44:fe | eth0: 5e:12:9f:77:01:aa

---

# Project Structure

macswap/
├── macswap.py
└── README.md

---

# Notes

Some network managers may restore the original MAC address automatically.

If MAC resets after changing:
- disable MAC randomization in NetworkManager
- or restart the interface manually

---

# TODO

- curses UI
- logging
- profiles
- systemd service
- GUI version
