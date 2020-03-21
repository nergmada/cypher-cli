import yaml
import os
import sys
from curses import wrapper
import curses
import shutil
from cli.ui import MenuWindow, DictWindow, Slider, SliderSet, SelectionWindow, InputBar
from cli.cypher import get_type_info, collate_abilities
from cli.markdown.player import generate_profile, generate_private_info

type_info = [yaml.safe_load(open("cypher/type/" + t + ".yaml", "r")) for t in ["adept", "explorer", "speaker", "warrior"]]
foci_info = [yaml.safe_load(open(f.path, "r")) for f in os.scandir("cypher/foci")]
flavour_info = [yaml.safe_load(open(f.path, "r")) for f in os.scandir("cypher/flavours")]



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
    players = []
    while True:
        stdscr.refresh()
        selection_window.render(stdscr)
        character = stdscr.getkey()
        selection_window.handle_input(character)
        if selection_window.was_enter_hit():
            break
    for character in selection_window.get_chosen():
        player_name = InputBar(stdscr)
        while True:
            stdscr.refresh(True)
            stdscr.addstr(4, 2, "Please enter the player name for " + character["identifier"] + ": ")
            player_name.render(stdscr)
            c = stdscr.getkey()
            player_name.handle_input(c)
            if c == "\n":
                break
        player = create_character(stdscr, logs, campaign, character)
        player["player_name"] = player_name.get_current_input()
        yaml.safe_dump(player, open(logs + "/players/" + player["player_name"] + ".yaml", "w"))
        players.append(player)
    return players
    

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
    
    profile["character_name"] = name_input.get_current_input()

    # Configure stats
    sliders = SliderSet(8, 2)
    stats = [(key, value) for key, value in get_type_info(profile["type"])["stats"].items()]
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
    #create a general stats
    profile["stats"] = {}
    for key, value in stats:
        profile["stats"][key] = sliders.get_slider(key).value()
    #create a pool
    profile["pool"] = profile["stats"].copy()
    
    # Warrior Might Vs Speed
    
    if profile["type"].lower() == "warrior":
        edge_selection = MenuWindow(stdscr)
        edge_selection.set_items([{'name' : "Might"}, {'name' : "Speed"}])
        edge_selection.set_message("Please choose the edge for the warrior class:")
        while True:
            stdscr.refresh()
            edge_selection.render(stdscr)
            c = stdscr.getkey()
            edge_selection.handle_input(c)
            if edge_selection.was_enter_hit():
                break
        if edge_selection.get_selected()["name"] == "Might":
            profile["edge"] = {
                "might": 1,
                "speed": 0,
                "intellect": 0
            }
        else:
            profile["edge"] = {
                "might": 0,
                "speed": 1,
                "intellect": 0
            }
    else:
        profile["edge"] = get_type_info(profile["type"])["edge"].copy()
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
    profile["clothing"] = clothing

    #select abilities
    abilities = collate_abilities(profile["type"], profile["focus"], profile["flavour"])[1]
    abilities = [{'name': ability} for ability in sorted(set(abilities))]

    abilities_choices = SelectionWindow(stdscr)
    abilities_choices.set_items(abilities)
    abilities_choices.set_limit(4)
    abilities_choices.set_message("Use arrows to select 4 abilities, then hit enter")
    while True:
        stdscr.refresh()
        abilities_choices.render(stdscr)
        character = stdscr.getkey()
        abilities_choices.handle_input(character)
        if len(abilities_choices.get_chosen()) == 4 and abilities_choices.was_enter_hit():
            break
        remaining = 4 - len(abilities_choices.get_chosen())
        abilities_choices.set_message("Use arrows to select " + str(remaining) +" abilities, then hit enter")
    profile["abilities"] = {}
    profile["abilities"][1] = [x["name"] for x in abilities_choices.get_chosen()]
    
    #set XP to zero
    profile["xp"] = 0
    return profile

def create_or_load_players(stdscr, logs, campaign):
    if check_for_players(logs):
        players = get_players(logs)
        generate_subconscious(players)
        return players
    else:
        players = create_characters(stdscr, logs, campaign)
        generate_subconscious(players)
        return players

def generate_subconscious(players):
    shutil.rmtree("subconscious")
    os.mkdir("subconscious")    
    for player in players:
        os.mkdir("subconscious/" + player["player_name"].lower())
        open("subconscious/" + player["player_name"].lower() + "/shared.md", "w").write(generate_profile(player))
        open("subconscious/" + player["player_name"].lower() + "/private.md", "w").write(generate_private_info(player))