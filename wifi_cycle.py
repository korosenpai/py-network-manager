# cycling through wifis in polybar

import json
import subprocess
import pathlib
from os import system, getcwd, chdir

# TODO: add cycle through wifis stored in computer automatically

# NOTE: getcwd() is current dir, pathlib is dir where we want to be (got it from __file__)
correct_path = str(pathlib.Path(__file__).parent.absolute())
if getcwd() != correct_path:
    chdir(correct_path)


with open("wifi.json", "r") as jsonfile:
    WIFI = json.load(jsonfile)


# run in terminal
def trun(command) -> tuple:
    return subprocess.check_output(command, shell=True).decode()


def available_wifi():
    return trun("nmcli dev wifi")[0]

def connected_to():
    return trun("nmcli -t -f NAME c show --active").removeprefix("Auto").strip()

def connect():
    idx = list(WIFI.keys()).index(connected_to()) + 1 if connected_to() else 0
    if idx >= len(WIFI):
        idx = 0


    connected = False
    while not connected:
        ssid = list(WIFI.keys())[idx]
        
        if ssid == connected_to():
            # if cycle back to same wifi, quit
            print("cycled all wifi, can connect to \033[91mnone\033[0m")
            break

        try:
            av = trun(f"nmcli dev wifi c '{ssid}' password '{WIFI[ssid]}'")
            print(f"connected to \033[92m'{ssid}'\033[0m")
            connected = True

        except Exception as e:
            # cycle to next wifi if cannot connect, dont connect to same wifi,
            idx = idx + 1 if idx + 1 < len(WIFI) else 0 


if __name__ == "__main__":
    #connect("TIM_MF90_1B3C", "896_DIP_ECS")
    #connect("it hurts when IP😩", "bennysmulpp")
    connect()
