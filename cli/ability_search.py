from curses import wrapper, ascii
import curses
import yaml 
import re

from cli.ui import InputBar, MenuWindow, DictWindow

abilities = yaml.safe_load(open("cypher/abilities.yaml"))

def get_all_abilities():
    return [x["name"] for x in abilities]

def ability_search(term):
    term = term.replace("_", " ")
    return [x for x in abilities if re.search(term.lower(), x["name"].lower())]


def search_abilities(stdscr):
    search_bar = InputBar(stdscr)
    menu_window = MenuWindow(stdscr)
    while True:
        stdscr.refresh(True)
        
        menu_window.set_items(ability_search(search_bar.get_current_input()))
        
        menu_window.render(stdscr)
        search_bar.render(stdscr)
        
        character = stdscr.getkey()

        search_bar.handle_input(character)
        menu_window.handle_input(character)

        if menu_window.was_enter_hit():
            render_result(stdscr, menu_window.get_selected())


def render_result(stdscr, result):
    dict_window = DictWindow([("name", "Name"), ("cost", "Cost"), ("activation", "Type"), ("description", "Description")])
    dict_window.set_item_to_render(result)
    while True:
        dict_window.render(stdscr)
        character = stdscr.getkey()
        dict_window.handle_input(character)
        if dict_window.was_backspace_hit():
            break


#wrapper(search_abilities)