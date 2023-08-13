import pyfiglet
from time import sleep

result = pyfiglet.figlet_format("wifi  manager", font = "slant")
print(f"{result}\n\nrunning nmcli dev wifi...")

sleep(2) # TODO: load available wifi

import curses
import subprocess
import pyglet

# Function to get available networks using nmcli
def get_networks():
    networks = []
    output = subprocess.check_output(['nmcli', 'device', 'wifi', 'list'], universal_newlines=True)
    lines = output.strip().split('\n')[1:]
    for line in lines:
        parts = line.split()
        networks.append((parts[0], parts[1], parts[6]))
    return networks

def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()

    # Create a Pyglet window with transparency
    window = pyglet.window.Window(width=80, height=24, style='borderless')
    window.set_location(stdscr.getbegyx()[1], stdscr.getbegyx()[0])

    @window.event
    def on_draw():
        window.clear()
        stdscr.refresh()

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Network Manager App", curses.A_BOLD)
        
        networks = get_networks()
        for idx, network in enumerate(networks, start=2):
            stdscr.addstr(idx, 0, f"{idx-1}. {network[0]} - {network[1]} ({network[2]})", curses.A_NORMAL)

        stdscr.addstr(len(networks) + 2, 0, "Press 'q' to quit", curses.A_BOLD)
        
        stdscr.refresh()
        
        key = stdscr.getch()
        if key == ord('q'):
            break

if __name__ == "__main__":
    curses.wrapper(main)

