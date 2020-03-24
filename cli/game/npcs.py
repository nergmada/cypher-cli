from cli.ui import MenuWindow, DictWindow, Slider, InputBar
from random import randrange


def get_new_health(stdscr, original):
    slider_bar = Slider(4, 2)
    slider_bar.set_range(0, original)
    slider_bar.set_current_value(original)
    while True:
        stdscr.refresh()
        stdscr.addstr(2, 2, "Reduce health then hit enter")
        slider_bar.render(stdscr)
        c = stdscr.getkey()
        slider_bar.handle_input(c)
        if c == "\n":
            break
    return slider_bar.value()

def log_npc_action(stdscr, npc, game, logger):
    log_input = InputBar(stdscr)
    while True:
        stdscr.refresh()
        log_input.render(stdscr)
        c = stdscr.getkey()
        log_input.handle_input(c)
        if c == "\n":
            break
    logger.write_log("[" + game["time"].strftime("%d/%m/%Y %H:%M:%S") + "]: (" + npc["name"] + ") " + log_input.get_current_input())


def generate_options(is_visible):
    return [
        {
            'name': 'Change health',
            'canonical': 'health'
        },
        {
            'name': 'Switch Visibility (visible: ' + str(is_visible) + ")",
            'canonical': 'visible'
        },
        {
            'name': 'Log Action',
            'canonical': 'log'
        },
        {
            'name': 'Go Back',
            'canonical': 'back'
        }
    ]

def handle_npc(stdscr, game, location, npc, logger):
    dict_window = DictWindow([
        ('name', 'Name'),
        ('level', 'Level'),
        ('health', 'Health'),
        ('armour', 'Armour'),
        ('damage', 'Damage'),
        ('modifiers', 'Mods'),
        ('description', 'Description')
    ])
    dict_window.set_item_to_render(location["npc_data"][npc])
    while True:
        dict_window.render(stdscr)
        c = stdscr.getkey()
        dict_window.handle_input(c)
        if dict_window.was_enter_hit():
            break
    menu = MenuWindow(stdscr)
    menu.set_items(generate_options(location["npc_data"][npc]["known"]))
    while True:
        stdscr.refresh()
        menu.render(stdscr)
        c = stdscr.getkey()
        menu.handle_input(c)
        if menu.was_enter_hit():
            if menu.get_selected()["canonical"] == "visible":
                location["npc_data"][npc]["known"] = not location["npc_data"][npc]["known"]
                menu.set_items(generate_options(location["npc_data"][npc]["known"]))
            elif menu.get_selected()["canonical"] == "health":
                location["npc_data"][npc]["health"] = get_new_health(stdscr, location["npc_data"][npc]["health"])
            elif menu.get_selected()["canonical"] == "log":
                log_npc_action(stdscr, location["npc_data"][npc], game, logger)
            elif menu.get_selected()["canonical"] == "back":
                break
            logger.save_location_data(location)

def npcs_menu(stdscr, game, location, logger):
    #Load NPCs into location data
    if "npc_data" not in location.keys():
        location["npc_data"] = {}
        for npc in location["npcs"]:
            if type(npc) is str:
                data = logger.get_npc_data(npc)
                if data is not None:
                    if type(data["name"]) is not str:
                        data["name"] = data["name"][randrange(0, len(data["name"]))]
                    location["npc_data"][npc] = data
        logger.save_location_data(location)
    menu = MenuWindow(stdscr)
    menu.set_items([x for x in location["npc_data"].values()])
    while True:
        stdscr.refresh()
        menu.render(stdscr)
        c = stdscr.getkey()
        menu.handle_input(c)
        if menu.was_enter_hit():
            break
    handle_npc(stdscr, game, location, menu.get_selected()["identifier"], logger)