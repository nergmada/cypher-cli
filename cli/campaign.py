import yaml
import os
from curses import wrapper
import curses
from cli.ui import MenuWindow


def choose_campaign(stdscr):
    campaigns = [yaml.safe_load(open(f.path + "/main.yaml")) for f in os.scandir("campaigns") if f.is_dir() and os.path.isfile(f.path + "/main.yaml") ]
    menu_window = MenuWindow(stdscr)
    menu_window.set_items(campaigns)
    while True:
        stdscr.refresh()

        menu_window.render(stdscr)
        character = stdscr.getkey()
        menu_window.handle_input(character)
        if menu_window.was_enter_hit():
            break
    stdscr.refresh()
    return menu_window.get_selected()

#wrapper(choose_campaign)
