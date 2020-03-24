import yaml
import os
from curses import wrapper
import curses
from cli.ui import MenuWindow, DictWindow, InputBar


class Logger:
    path = ""
    log = None
    def __init__(self, p, data = None, read_only = False):
        self.path = p
        if not read_only:
            if not os.path.exists(self.path):
                os.mkdir(self.path)
            if data is not None:
                yaml.dump(data, open(result + "/main.yaml", "w"))
            self.log = open(self.path + "/log.txt", "a")
        else:
            self.log = open(self.path + "/log.txt", "r")

    def has_main_file(self):
        return os.path.isfile(self.path + "/main.yaml")

    def get_campaign(self):
        return yaml.safe_load(open(self.path + "/main.yaml", "r"))["campaign"]
    
    def save_game(self, game):
        yaml.safe_dump(game, open(self.path + "/main.yaml", "w"))
    
    def load_game(self):
        return yaml.safe_load(open(self.path + "/main.yaml", "r"))

    def save_player_data(self, player):
        if not os.path.exists(self.path + "/players"):
            os.mkdir(self.path + "/players")
        yaml.safe_dump(player, open(self.path + "/players/" + player["player_name"] + ".yaml", "w"))

    def get_players(self):
        return [yaml.safe_load(open(x.path)) for x in os.scandir(self.path + "/players")]

    def has_players(self):
        if not os.path.isdir(self.path + "/players"):
            return False
        for x in os.scandir(self.path + "/players"):
            return True
        return False

    def load_player_data(self, name):
        players = [yaml.safe_load(open(x.path)) for x in os.scandir(self.path + "/players")]
        individual = [x for x in players if x["player_name"].lower() == name.lower()]
        if len(individual) == 0:
            return None
        return individual[0]
    
    def load_location_data(self, region, setting):
        if not os.path.exists(self.path + "/locations"):
            os.mkdir(self.path + "/locations")
        if not os.path.exists(self.path + "/locations/" + region):
            os.mkdir(self.path + "/locations/" + region)
        if not os.path.exists(self.path + "/locations/" + region + "/" + setting + ".yaml"):
            f = open("campaigns/" + self.get_campaign() + "/locations/" + region + "/" + setting + ".yaml", "r")
            w = open(self.path + "/locations/" + region + "/" + setting + ".yaml", "w")
            w.write(f.read())
            w.close()
        return yaml.safe_load(open(self.path + "/locations/" + region + "/" + setting + ".yaml", "r"))

    def save_location_data(self, data):
        yaml.safe_dump(data, open(self.path + "/locations/" + data["region"] + "/" + data["setting"] + ".yaml", "w"))

    def get_npc_data(self, name):
        if os.path.exists("campaigns/" + self.get_campaign() + "/npcs/" + name + ".yaml"):
            return yaml.safe_load(open("campaigns/" + self.get_campaign() + "/npcs/" + name + ".yaml", "r"))
        else:
            return "campaigns/" + self.get_campaign() + "/npcs/" + name + ".yaml"

    def write_log(self, txt):
        self.log.write(txt + "\n")
        self.log.flush()
    
    def read_log(self):
        return self.log.readlines()
    


def choose_or_create_log(stdscr, campaign):
    all_logs = [Logger(f.path) for f in os.scandir("logs") if f.is_dir() and os.path.isfile(f.path + "/main.yaml") ]
    campaign_logs = [x.load_game() for x in all_logs if x.get_campaign() == campaign["name"]]
    campaign_logs.insert(0, {"name": "Create New Log", "new_save": True})
    
    menu_window = MenuWindow(stdscr)
    menu_window.set_items(campaign_logs)
    while True:
        stdscr.refresh()
        menu_window.render(stdscr)
        
        character = stdscr.getkey()
        menu_window.handle_input(character)
        if menu_window.was_enter_hit():
            break
    if "new_save" in menu_window.get_selected().keys():
        while True:
            dict_window = DictWindow([("name", "Campaign Name"), ("author", "Author"), ("description", "Description")])
            dict_window.set_item_to_render(campaign)
            input_bar = InputBar(stdscr)
            while True:
                dict_window.render(stdscr)
                input_bar.render(stdscr)
                character = stdscr.getkey()
                input_bar.handle_input(character)
                if character == "\n":
                    break
            confirm_window = MenuWindow(stdscr)
            confirm_window.set_items([{'name': 'yes'}, {'name':'no'}])
            confirm_window.set_message("Please confirm new log name as '" + input_bar.get_current_input() + "' (overwrites):")
            while True:
                stdscr.refresh()
                confirm_window.render(stdscr)
                character = stdscr.getkey()
                confirm_window.handle_input(character)
                if confirm_window.was_enter_hit():
                    break
            if confirm_window.get_selected()['name'] == 'yes':
                break
        return Logger("logs/" + input_bar.get_current_input())
    else:
        return Logger("logs/" + menu_window.get_selected()["name"])
        
    
#wrapper(choose_or_create_log)
