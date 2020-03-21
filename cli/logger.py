import yaml
import os
from curses import wrapper
import curses
from cli.ui import MenuWindow, DictWindow, InputBar

def choose_or_create_log(stdscr, campaign):
    all_logs = [yaml.safe_load(open(f.path + "/main.yaml", "r").read()) for f in os.scandir("logs") if f.is_dir() and os.path.isfile(f.path + "/main.yaml") ]
    campaign_logs = [x for x in all_logs if x["campaign"] == campaign["name"]]
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
    if "new_save" in menu_window.get_selected():
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
        if not os.path.exists("logs/" + input_bar.get_current_input()):
            os.mkdir("logs/" + input_bar.get_current_input())
        result = "logs/" + input_bar.get_current_input()
        yaml.dump({'name': input_bar.get_current_input(), 'campaign': campaign["name"]}, open(result + "/main.yaml", "w"))
        return result
    else:
        result = "logs/" + menu_window.get_selected()["name"]
        return result
        
    
#wrapper(choose_or_create_log)
