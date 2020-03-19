#!/usr/bin/env python3

from cli.campaign import choose_campaign
from cli.logger import choose_or_create_log
from cli.generate_players import create_or_load_players

from curses import wrapper
from cli.ui import DictWindow, InputBar, SafeRenderScreen

def main(scr):
    stdscr = SafeRenderScreen(scr)
    campaign = choose_campaign(stdscr)
    logs = choose_or_create_log(stdscr, campaign)
    return create_or_load_players(stdscr, logs, campaign)

print(wrapper(main))