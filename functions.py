import subprocess
from os import system
from os.path import isfile

def to_raw(string) -> str:
    return fr"{string}"

# run in terminal
def trun(command) -> tuple:
    return subprocess.check_output(command, shell=True).decode()


def connect(wifi, pwd="") -> bool:
    try:
        trun(f"nmcli dev wifi c '{wifi}' ")
        print(f"connected to \033[92m'{wifi}'\033[0m")
        return True

    except:
        return False

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

def create_saved_wifi_dict():
    wifis = {}
    for wifi in get_available_saved_wifi():
        #print(wifi, " : ", get_saved_wifi_password(wifi))
        wifis[wifi] = get_saved_wifi_password(wifi).removesuffix("\n")
    
    return wifis


# create qr and show password of current wifi connected
def create_qr():
    msg = "nmcli dev wifi show-password"
    system(msg) # show in terminal with qr
    return trun(msg)



if __name__ == "__main__":
    #print(get_available_saved_wifi())
    #print(create_saved_wifi_dict())
    #create_qr()

    connect(get_available_saved_wifi()[0])
