import subprocess
from os import system

def to_raw(string) -> str:
    return fr"{string}"

# run in terminal
def trun(command) -> tuple:
    return subprocess.check_output(command, shell=True).decode()


def get_available_saved_wifi() -> list:
    wifis = (
        trun("nmcli -g NAME connection show")
        .replace("\\", "")
        .split("\n")
    )[:-1] # remove empty space
    #wifis = list(filter(lambda x: x != "", wifis))
    wifis = list(filter(lambda x: x.split(" ")[0] != "Wired", wifis)) # wired wifis dont have passwords

    return wifis

def get_saved_wifi_password(wifi):
    try:
        return trun(f"nmcli -s -g 802-11-wireless-security.psk connection show '{wifi}'")

    except Exception as e:
        #print(e)
        #return "error: not found"
        return

# create qr and show password of current wifi connected
def create_qr():
    msg = "nmcli dev wifi show-password"
    system(msg) # show in terminal with qr
    return trun(msg)



if __name__ == "__main__":
    print(get_available_saved_wifi())

    for wifi in get_available_saved_wifi():
        print(wifi, " : ", get_saved_wifi_password(wifi))