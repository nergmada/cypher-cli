import yaml
import os
from curses import wrapper
import curses



def render_campaigns(stdscr, campaigns, selected):
    my, mx = stdscr.getmaxyx()
    stdscr.clear()
    stdscr.border("#", "#", "#", "#")
    stdscr.addstr(2, 2, "please select a campaign: ")
    max_list = min([len(campaigns), my - 4])
    for i in range(0, max_list):
        if selected == i:
            stdscr.addstr(3+i, 2, "> " + campaigns[i]["name"])
        else: 
            stdscr.addstr(3+i, 2, campaigns[i]["name"])

def choose_campaign(stdscr):
    campaigns = [yaml.safe_load(open(f.path + "/main.yaml")) for f in os.scandir("campaigns") if f.is_dir() and os.path.isfile(f.path + "/main.yaml") ]
    my, mx = stdscr.getmaxyx()
    stdscr.clear()
    stdscr.border("#", "#", "#", "#")
    curses.curs_set(0)
    
    selected = 0
    if len(campaigns) == 0:
        stdscr.addstr(2, 2, "No campaigns found in 'campaigns/' ")
    else:
        render_campaigns(stdscr, campaigns, selected)
    while True:
        character = stdscr.getkey()
        if character == "\n":
            break
        elif character == "KEY_UP" and selected > 0:
            selected -= 1
        elif character == "KEY_DOWN" and selected < len(campaigns) - 1:
            selected += 1
    return campaigns[selected]

wrapper(choose_campaign)