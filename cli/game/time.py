from datetime import timedelta

from cli.ui import MenuWindow

options = [
    {
        'name': 'Add 10 seconds',
        'canonical': 'seconds',
        'delta': timedelta(seconds=10)
    },
    {
        'name': 'Add 1 minute',
        'canonical': 'minute',
        'delta': timedelta(minutes=1)
    },
    {
        'name': 'Add 10 minutes',
        'canonical': 'minutes',
        'delta': timedelta(minutes=10)
    },
    {
        'name': 'Add 1 hour',
        'canonical': 'hour',
        'delta': timedelta(hours=1)
    },
    {
        'name': 'Add 6 hours',
        'canonical': 'hours',
        'delta': timedelta(hours=6)
    },
    {
        'name': 'Add 1 day',
        'canonical': 'day',
        'delta': timedelta(days=1)
    },
    {
        'name': 'Go Back',
        'canonical': 'back'
    },
]

def time_menu(stdscr, game, campaign):
    if "time" not in game.keys():
        game["time"] = campaign["time"]
    menu = MenuWindow(stdscr)
    menu.set_items(options)
    while True:
        menu.set_message("Current time: " + game["time"].strftime("%d/%m/%Y %H:%M:%S"))
        menu.render(stdscr)
        c = stdscr.getkey()
        menu.handle_input(c)
        if menu.was_enter_hit():
            if menu.get_selected()["canonical"] == 'back':
                break
            else:
                game["time"] += menu.get_selected()["delta"]
