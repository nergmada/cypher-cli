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
import os
from cli.ui import MenuWindow
from cli.game.time import time_menu
from cli.game.player import player_menu
from cli.game.location import display_location

options = [
    {
        'name': 'Player Options',
        'canonical': 'player'
    },
    {
        'name': 'Change Time',
        'canonical': 'time'
    },
    {
        'name': 'Move All Players',
        'canonical': 'move'
    },
    {
        'name': 'Save and Exit',
        'canonical': 'exit'
    }
]


def move_all_players(stdscr, players, logger):
    regions = [{"name" : x.name} for x in os.scandir(f"campaigns/{logger.get_campaign()}/locations")]
    region_menu = MenuWindow(stdscr)
    region_menu.set_items(regions)
    while True:
        stdscr.refresh()
        region_menu.render(stdscr)
        c = stdscr.getkey()
        region_menu.handle_input(c)
        if region_menu.was_enter_hit():
            break
    settings = [{"name" : x.name.split(".")[0]} for x in os.scandir(f"campaigns/{logger.get_campaign()}/locations/{region_menu.get_selected()['name']}")]
    setting_menu = MenuWindow(stdscr)
    setting_menu.set_items(settings)
    while True:
        stdscr.refresh()
        setting_menu.render(stdscr)
        c = stdscr.getkey()
        setting_menu.handle_input(c)
        if setting_menu.was_enter_hit():
            break
    for player in players:
        player["location"]["region"] = region_menu.get_selected()["name"]
        player["location"]["setting"] = setting_menu.get_selected()["name"]
        logger.save_player_data(player)
    
    location = logger.load_location_data(region_menu.get_selected()["name"], setting_menu.get_selected()["name"])
    display_location(stdscr, location)

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
            if menu.get_selected()["canonical"] == "move":
                move_all_players(stdscr, players, logger)
            if menu.get_selected()["canonical"] == "exit":
                logger.save_game(game)
                for player in players:
                    logger.save_player_data(player)
                exit(0)
            logger.save_game(game)