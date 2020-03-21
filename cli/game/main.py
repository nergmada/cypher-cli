#Menu
# get location info
    # change location
    # return 
# get NPC Info
    # change NPC
    # return
# get item info
    # change item
    # add new item
    # return
# get Player Info
    # change player info
    # Log player action
# Change Time

from cli.ui import MenuWindow
from cli.game.time import time_menu

options = [
    {
        'name': 'Location Options',
        'canonical': 'location'
    },
    {
        'name': 'NPC Options',
        'canonical': 'npc'
    },
    {
        'name': 'Item Options',
        'canonical': 'item'
    },
    {
        'name': 'Player Options',
        'canonical': 'player'
    },
    {
        'name': 'Change Time',
        'canonical': 'time'
    }
]

def play_game(stdscr, campaign, players, logs):
    game = {}
    menu = MenuWindow(stdscr)
    menu.set_items(options)
    while True:
        stdscr.refresh()
        menu.render(stdscr)
        c = stdscr.getkey()
        menu.handle_input(c)
        if menu.was_enter_hit():
            if menu.get_selected()["canonical"] == "time":
                time_menu(stdscr, game, campaign)