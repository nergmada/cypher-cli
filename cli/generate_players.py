import yaml
import os
from curses import wrapper
import curses
from cli.ui import MenuWindow, DictWindow, Slider, SliderSet, SelectionWindow, InputBar

type_info = [yaml.safe_load(open("cypher/type/" + t + ".yaml", "r")) for t in ["adept", "explorer", "speaker", "warrior"]]

def check_for_players(log_dir):
    result = os.path.isdir(log_dir + "/players")
    if not result:
        os.mkdir(log_dir + "/players")
    for x in os.scandir(log_dir + "/players"):
        return True
    return False

def get_players(log_dir):
    return [yaml.safe_load(open(x.path)) for x in os.scandir(log_dir + "/players")]

def get_characters(campaign_dir):
    return [yaml.safe_load(open(x.path)) for x in os.scandir(campaign_dir + "/characters")]


def create_characters(stdscr, logs, campaign):
    characters = get_characters("campaigns/" + campaign["name"])
    selection_window = SelectionWindow(stdscr)
    selection_window.set_items(characters, "identifier")
    while True:
        stdscr.refresh()
        selection_window.render(stdscr)
        character = stdscr.getkey()
        selection_window.handle_input(character)
        if selection_window.was_enter_hit():
            break
    for character in selection_window.get_chosen():
        create_character(stdscr, logs, campaign, character)

def calculate_remaining_and_update_range(stats, sliders):
    min_value = sum([value for key, value in stats], 0)
    current_value = sum([sliders.get_slider(key).value() for key, value in stats])
    remaining =  6 - (current_value - min_value)
    for key, value in stats:
        sliders.get_slider(key).set_range(value, sliders.get_slider(key).value() + remaining)
    return remaining

def create_character(stdscr, logs, campaign, profile):
    #Show player profile and description
    listing_order = [("identifier", "Name"), ("type", "Type"), ("focus", "Focus"), ("flavour", "Flavour"), ("descriptor", "Descriptor"), ("description", "Description")]
    dict_window = DictWindow(listing_order)
    dict_window.set_item_to_render(profile)
    
    while True:
        dict_window.render(stdscr)
        stdscr.addstr(stdscr.getmaxyx()[0]-2, 2, "Hit Enter to Continue")
        character = stdscr.getkey()
        dict_window.handle_input(character)
        if dict_window.was_enter_hit():
            break
    
    dict_window.set_listing_order(listing_order[:3])

    #Get player character name
    name_input = InputBar(stdscr)
    while True:
        dict_window.render(stdscr, True)
        stdscr.addstr(8, 2, "Please enter a name and hit enter: ")
        name_input.render(stdscr)
        character = stdscr.getkey()
        dict_window.handle_input(character)
        name_input.handle_input(character)
        if dict_window.was_enter_hit():
            break

    # Configure stats
    sliders = SliderSet(8, 2)
    stats = [("might", 10), ("speed", 10), ("intellect", 10)]
    for stat in stats:
        sliders.add_slider(stat[0])
        sliders.get_slider(stat[0]).set_current_value(stat[1])
    
    while True:
        stdscr.refresh()
        remaining = calculate_remaining_and_update_range(stats, sliders)
        dict_window.render(stdscr)
        sliders.render(stdscr)
        if remaining > 0:
            stdscr.addstr(15, 4, "Remaining Points: " + str(remaining))
        else:
            stdscr.addstr(15, 4, "Press Enter to continue")
        character = stdscr.getkey()
        sliders.handle_input(character)
        if remaining == 0 and character == "\n":
            break
            
    #Clothing
    clothing = []
    clothing_input = InputBar(stdscr)

    while True:
        dict_window.render(stdscr, True)
        stdscr.addstr(8, 2, "Clothing: ")
        stdscr.addstr(9, 2, ", ".join(clothing))
        stdscr.addstr(11, 2, "Type and hit enter to add, or hit enter when clear to continue")
        clothing_input.render(stdscr)
        character = stdscr.getkey()
        dict_window.handle_input(character)
        clothing_input.handle_input(character)
        if dict_window.was_enter_hit():
            if len(clothing_input.get_current_input()) == 0:
                break
            else:
                clothing.append(clothing_input.get_current_input())
                clothing_input.set_current_input("")

    #select abilities


def create_or_load_players(stdscr, logs, campaign):
    if check_for_players(logs[0]):
        players = get_players(logs[0])
    else:
        create_characters(stdscr, logs, campaign)