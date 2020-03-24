#!/usr/bin/env python3
from curses import wrapper

from cli.campaign import choose_campaign
from cli.logger import choose_or_create_log
from cli.players import create_or_load_players
from cli.ui import DictWindow, InputBar, SafeRenderScreen
from cli.game.main import play_game



def main(scr):
    stdscr = SafeRenderScreen(scr)
    campaign = choose_campaign(stdscr)
    logs = choose_or_create_log(stdscr, campaign)
    players = create_or_load_players(stdscr, logs, campaign)
    play_game(stdscr, campaign, players, logs)
print(wrapper(main))