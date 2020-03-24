#Menu 
# get Player Info
    # change location
        # change NPC
        # change item
        # add new item
    # change inventory
        # 
    # change player info
    # Log player action
    # return 
# search abilities
# Change Time
# exit
import yaml
from cli.ui import MenuWindow
from cli.game.time import time_menu
from cli.game.player import player_menu

options = [
    {
        'name': 'Player Options',
        'canonical': 'player'
    },
    {
        'name': 'Change Time',
        'canonical': 'time'
    }
]

def save_game(game, logs):
    yaml.safe_dump(game, open(logs + "/main.yaml", "w"))
    

def add_important_info_to_game(game, campaign):
    if "time" not in game.keys():
        game["time"] = campaign["time"]

def play_game(stdscr, campaign, players, logger):
    game = logger.load_game()
    add_important_info_to_game(game, campaign)
    logger.save_game(game)

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
            if menu.get_selected()["canonical"] == "player":
                player_menu(stdscr, game, campaign, players, logger)
            logger.save_game(game)