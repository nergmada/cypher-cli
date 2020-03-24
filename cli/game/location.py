from cli.ui import DictWindow, MenuWindow, MultiDictWindow
from cli.game.npcs import npcs_menu

options = [
    {
        'name': 'View Location NPCs',
        'canonical': 'npcs'
    },
    {
        'name': 'View Location Items',
        'canonical': 'items'
    },
    {
        'name': 'Change Location',
        'canonical': 'change'
    },
    {
        'name': 'Go Back',
        'canonical': 'back'
    }
]

def list_room_items(stdscr, location):
    multi_dict_window = MultiDictWindow(location["items"])
    multi_dict_window.set_listing_order([
        ('name', 'Name'),
        ('description', 'Description')
    ])
    while True:
        multi_dict_window.render(stdscr)
        c = stdscr.getkey()
        multi_dict_window.handle_input(c)
        if multi_dict_window.was_backspace_hit():
            break

def change_location(stdscr, game, player, logger, current_location):
    next_locations = []
    for location in current_location["adjacent"]:
        region_setting = location.split("/")
        if len(region_setting) > 1:
            next_locations.append({
                'location': {
                    'region': region_setting[0],
                    'setting': region_setting[1]
                },
                'name': region_setting[0] + " -> " + region_setting[1]
            })
        else:
            next_locations.append({
                'location': {
                    'region': current_location["region"],
                    'setting': region_setting[0]
                },
                'name': region_setting[0]
            })
    menu = MenuWindow(stdscr)
    menu.set_items(next_locations)
    while True:
        stdscr.refresh()
        menu.render(stdscr)
        c = stdscr.getkey()
        menu.handle_input(c)
        if menu.was_enter_hit():
            break
    player["location"] = menu.get_selected()["location"]
    logger.save_player_data(player)
    location_menu(stdscr, game, player, logger)


def location_menu(stdscr, game, player, logger):
    location = logger.load_location_data(player["location"]["region"], player["location"]["setting"])
    dict_window = DictWindow([
        ('name', 'Name'), 
        ('lighting', 'Lighting'), 
        ('gravity', 'Gravity'), 
        ('scale', 'Scale'),
        #('elemental', 'Elemental'), - Elemental features are additive
        ('description', 'Description')
        ])
    dict_window.set_item_to_render(location)
    while True:
        dict_window.render(stdscr)
        c = stdscr.getkey()
        dict_window.handle_input(c)
        if dict_window.was_enter_hit():
            break

    menu = MenuWindow(stdscr)
    menu.set_items(options)
    while True:
        stdscr.refresh()
        menu.render(stdscr)
        c = stdscr.getkey()
        menu.handle_input(c)
        if menu.was_enter_hit():
            if menu.get_selected()["canonical"] == "npcs":
                npcs_menu(stdscr, game, location, logger)
            elif menu.get_selected()["canonical"] == "items":
                list_room_items(stdscr, location)
            elif menu.get_selected()["canonical"] == "change":
                change_location(stdscr, game, player, logger, location)
                break
            elif menu.get_selected()["canonical"] == "back":
                break

    # change NPC
    # change item
    # add new item
    # change location