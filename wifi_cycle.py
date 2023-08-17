# cycling through wifis in polybar

import json
import subprocess
import pathlib
from os import system, getcwd, chdir

from functions import trun, create_saved_wifi_dict

# move place to this correct dir if run from somewhere else: ex polybar
# NOTE: getcwd() is current dir, pathlib is dir where we want to be (got it from __file__)
correct_path = str(pathlib.Path(__file__).parent.absolute())
if getcwd() != correct_path:
    chdir(correct_path)


WIFI = create_saved_wifi_dict()


def connected_to():
    return trun("nmcli -t -f NAME c show --active").strip()


def connect():
    idx = list(WIFI.keys()).index(connected_to()) + 1 if connected_to() and connected_to() in WIFI.keys() else 0
    if idx >= len(WIFI):
        idx = 0

    starting_ssid =  list(WIFI.keys())[idx - 1]

    connected = False
    while not connected:
        ssid = list(WIFI.keys())[idx]
        
        if ssid == starting_ssid:
            # if cycle back to same wifi, quit
            print("cycled all wifi, can connect to \033[91mnone\033[0m")
            trun(f"notify-send 'cannot connect to any wifi...'")
            break

        try:
            av = trun(f"nmcli dev wifi c '{ssid.removeprefix('Auto ')}' password '{WIFI[ssid]}'")
            print(f"connected to \033[92m'{ssid}'\033[0m")
            trun(f"notify-send 'connected to' '{ssid}'")
            connected = True

        except Exception as e:
            # cycle to next wifi if cannot connect, dont connect to same wifi,
            idx = idx + 1 if idx + 1 < len(WIFI) else 0 


if __name__ == "__main__":
    print(f"currently connected to: '{connected_to()}'\n")
    connect()
