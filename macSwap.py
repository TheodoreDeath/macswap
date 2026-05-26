import sys
import subprocess
import time
import os

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

DRY_RUN = "--dry-run" in sys.argv


def run(cmd):
    if DRY_RUN:
        print(f"[DRY] {' '.join(cmd)}")
        return
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def clear():
    os.system("clear")


def check_root():
    if DRY_RUN:
        return
    if os.geteuid() != 0:
        print(f"{RED}Run as root (sudo){RESET}")
        sys.exit(1)


def get_interfaces():
    return os.listdir("/sys/class/net/")


def interface_exists(iface):
    return os.path.exists(f"/sys/class/net/{iface}")


def get_mac(iface):
    if DRY_RUN:
        return "DRY:XX:XX:XX:XX:XX"
    try:
        with open(f"/sys/class/net/{iface}/address") as f:
            return f.read().strip()
    except:
        return "unknown"


def status_line(ifaces):
    return " | ".join([f"{i}: {get_mac(i)}" for i in ifaces])


def parse_time(t):
    unit = t[-1]
    value = int(t[:-1])
    return {
        "s": value,
        "m": value * 60,
        "h": value * 3600
    }.get(unit, None)

def set_mac(iface, option, mac=None):
    run(["ip", "link", "set", iface, "down"])

    if option == "-r":
        run(["macchanger", "-r", iface])
    elif option == "-e":
        run(["macchanger", "-e", iface])
    elif option == "-m":
        run(["macchanger", "-m", mac, iface])

    run(["ip", "link", "set", iface, "up"])


def auto_mode(ifaces, option, interval, mac=None):
    print(f"{GREEN}Auto mode (Ctrl+C to stop){RESET}")
    try:
        while True:
            for iface in ifaces:
                set_mac(iface, option, mac)

            print(f"\r{YELLOW}{status_line(ifaces)}{RESET}", end="")
            time.sleep(interval)

    except KeyboardInterrupt:
        print(f"\n{RED}Stopped{RESET}")

def select_interfaces():
    interfaces = get_interfaces()

    print(f"{GREEN}Available interfaces:{RESET}")
    for i, iface in enumerate(interfaces):
        print(f"{i}) {iface}")

    choice = input("\nSelect (e.g. 0 or 0,1): ").strip()

    selected = []
    for i in choice.split(","):
        try:
            selected.append(interfaces[int(i)])
        except:
            pass

    return selected


def menu():
    while True:
        clear()
        print(f"{GREEN}=== MACSWAP MENU ==={RESET}")
        print("1) Random MAC")
        print("2) Random MAC (same vendor)")
        print("3) Set custom MAC")
        print("4) Auto mode")
        print("5) Exit")

        choice = input("\nSelect: ").strip()

        if choice == "5":
            sys.exit(0)

        if choice not in ["1", "2", "3", "4"]:
            continue

        ifaces = select_interfaces()
        if not ifaces:
            input("No interfaces selected...")
            continue

        mac = None
        interval = None

        if choice == "1":
            option = "-r"

        elif choice == "2":
            option = "-e"

        elif choice == "3":
            option = "-m"
            mac = input("Enter MAC: ").strip()

        elif choice == "4":
            option = "-r"
            t = input("Interval (e.g. 10s, 1m): ")
            interval = parse_time(t)

        clear()

        if interval:
            auto_mode(ifaces, option, interval, mac)
        else:
            for iface in ifaces:
                set_mac(iface, option, mac)

            print(status_line(ifaces))
            input("\nDone. Press Enter...")

def cli_mode():
    args = sys.argv[1:]

    if "-?" in args or "--help" in args:
        print("Usage:")
        print(" python macswap.py wlan0 eth0 -r")
        print(" python macswap.py wlan0 -m 00:11:22:33:44:55")
        print(" python macswap.py wlan0 -r -t 5m")
        print(" python macswap.py --dry-run")
        sys.exit(0)

    options = ["-r", "-e", "-m"]

    option = next((a for a in args if a in options), None)

    if not option:
        print("No option provided")
        sys.exit(1)

    option_index = args.index(option)
    ifaces = args[:option_index]

    for iface in ifaces:
        if not interface_exists(iface):
            print(f"Interface {iface} not found")
            sys.exit(1)

    mac = None
    interval = None

    if option == "-m":
        mac = args[option_index + 1]

    if "-t" in args:
        t = args[args.index("-t") + 1]
        interval = parse_time(t)

    if interval:
        auto_mode(ifaces, option, interval, mac)
    else:
        for iface in ifaces:
            set_mac(iface, option, mac)

        print(status_line(ifaces))


def main():
    check_root()

    if len(sys.argv) == 1:
        menu()  # 🔥 запуск меню
    else:
        cli_mode()


if __name__ == "__main__":
    main()
