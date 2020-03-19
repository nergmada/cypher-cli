from curses import wrapper, ascii
import curses
import yaml 
import re

abilities = yaml.safe_load(open("cypher/abilities.yaml"))

def search(term):
    return [x for x in abilities if re.search(term.lower(), x["name"].lower())]


def render_static(stdscr, search_term, results, selector):
    stdscr.clear()
    my, mx = stdscr.getmaxyx()
    items = min([len(results), my-2])
    for i in range(0, items):
        if i == selector:
            stdscr.addstr(i, 0, "> " + results[i]["name"])
        else:
            stdscr.addstr(i, 0, results[i]["name"])
    stdscr.addstr(my-2, 0, "#" * (mx-1))
    stdscr.addstr(my-1, 0, search_term)
    stdscr.move(my-1, len(search_term))

def search_abilities(stdscr):
    my, mx = stdscr.getmaxyx()
    curses.noecho()
    #Get curses to do key conversion
    stdscr.keypad(True)
    
    search_input = ""
    selected = 0
    search_results = search(search_input)
    render_static(stdscr, search_input, search_results, selected)
    while True:
        character = stdscr.getkey()
        
        if len(character) > 1:
            if "KEY_BACKSPACE" == character:
                search_input = search_input[:-1]
                search_results = search(search_input)
                selected = 0
            elif "KEY_DOWN" == character and selected < len(search_results) - 1:
                selected += 1
            elif "KEY_UP" == character and selected > 0:
                selected -= 1
            else:
                if len(search_results) > 0:
                    render_result(stdscr, search_results[selected])
                else:
                    curses.beep()
        elif character == "\n":
            if len(search_results) > 0:
                render_result(stdscr, search_results[selected])
            else:
                curses.beep()
        elif ascii.isalnum(character) or ascii.isspace(character):
            search_input += character
            search_results = search(search_input)
            selected = 0
        render_static(stdscr, search_input, search_results, selected)

def render_result(stdscr, result):
    stdscr.clear()
    stdscr.border("#", "#", "#", "#")
    curses.curs_set(0)
    
    my, mx = stdscr.getmaxyx()
    
    stdscr.addstr(2, 2, "name: " + result["name"])
    stdscr.addstr(4, 2, "cost: " + result["cost"])
    stdscr.addstr(6, 2, "type: " + result["activation"])
    stdscr.addstr(8, 2, "description: ")
    
    sentences = [(result["description"][i:i+mx-4]) for i in range(0, len(result["description"]), mx-4)]
    for i in range(0, len(sentences)):
        stdscr.addstr(9+i, 2, sentences[i])

    while True:
        character = stdscr.getkey()
        if len(character) > 1 and character == "KEY_BACKSPACE":
            break
    curses.curs_set(1)


wrapper(search_abilities)