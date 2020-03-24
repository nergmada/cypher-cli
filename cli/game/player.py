
# change location
    # change NPC
    # change item
    # add new item
# change inventory
    # add item
    # remove item
# Log player action
# change points
# return 

from cli.ui import MenuWindow, SliderSet, Slider, InputBar
from cli.game.location import location_menu

options = [
    {
        'name': 'Location Options',
        'canonical': 'location'
    },
    {
        'name': 'Log Player Action',
        'canonical': 'log'
    },
    {
        'name': 'Change Points',
        'canonical': 'points'
    },
    {
        'name': 'Reveal Update',
        'canonical': 'update'
    },
    {
        'name': 'Go Back',
        'canonical': 'back'
    }
]

def log_player_action(stdscr, player, game, logger):
    log_input = InputBar(stdscr)
    while True:
        stdscr.refresh()
        log_input.render(stdscr)
        c = stdscr.getkey()
        log_input.handle_input(c)
        if c == "\n":
            break
    logger.write_log("[" + game["time"].strftime("%d/%m/%Y %H:%M:%S") + "]: (" + player["character_name"] + ") " + log_input.get_current_input())

def change_points(stdscr, player):
    sliders = SliderSet(8, 2)
    for stat, max_value in player["stats"].items():
        sliders.add_slider(stat)
        sliders.get_slider(stat).set_range(0, max_value)
        sliders.get_slider(stat).set_current_value(player["pool"][stat])
    while True:
        stdscr.refresh()
        sliders.render(stdscr)
        c = stdscr.getkey()
        sliders.handle_input(c)
        if c == "\n":
            break
    for stat, max_value in player["stats"].items():
        player["pool"][stat] = sliders.get_slider(stat).value()

def push_update(stdscr, player):
    menu_window = MenuWindow(stdscr)
    menu_window.set_items(player["updates"]) 
    while True:
        stdscr.refresh()
        menu_window.render(stdscr)
        c = stdscr.getkey()
        menu_window.handle_input(c)
        if menu_window.was_enter_hit():
            break
        elif c == "KEY_BACKSPACE":
            return None
    if "live" not in player.keys():
        player["live"] = []
    player["live"].append(menu_window.get_selected())

def player_options(stdscr, game, campaign, player, logger):
    option_menu = MenuWindow(stdscr)
    option_menu.set_items(options)
    while True:
        stdscr.refresh()
        option_menu.render(stdscr)
        c = stdscr.getkey()
        option_menu.handle_input(c)
        if option_menu.was_enter_hit():
            if option_menu.get_selected()["canonical"] == "back":
                break
            elif option_menu.get_selected()["canonical"] == "points":
                change_points(stdscr, player)
            elif option_menu.get_selected()["canonical"] == "log":
                log_player_action(stdscr, player, game, logger)
            elif option_menu.get_selected()["canonical"] == "location":
                location_menu(stdscr, game, player, logger)
            elif option_menu.get_selected()["canonical"] == "update":
                if "updates" in player.keys():
                    push_update(stdscr, player)
            logger.save_player_data(player)


def player_menu(stdscr, game, campaign, players, logger):
    player_menu = MenuWindow(stdscr)
    player_menu.set_items(players, "character_name")
    while True:
        stdscr.refresh()
        player_menu.render(stdscr)
        c = stdscr.getkey()
        player_menu.handle_input(c)
        if player_menu.was_enter_hit():
            break
    player_options(stdscr, game, campaign, player_menu.get_selected(), logger)