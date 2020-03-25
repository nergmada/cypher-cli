import curses

class SafeRenderScreen:
    screen = None
    def __init__(self, stdscr):
        self.screen = stdscr
        self.keypad = stdscr.keypad
        self.getkey = stdscr.getkey
        self.clear = stdscr.clear
        self.border = stdscr.border
        self.getmaxyx = stdscr.getmaxyx

    def refresh(self, with_cursor = False):
        self.screen.clear()
        self.screen.border("#", "#", "#", "#")
        if with_cursor:
            curses.curs_set(1)
        else:
            curses.curs_set(0)

    def addstr(self, y, x, txt, attr = curses.A_NORMAL):
        my, mx = self.screen.getmaxyx()
        if y >= 0 and y < my - 1 and x >= 0 and x + len(txt) < mx:
            self.screen.addstr(y, x, txt, attr)
    
    def move(self, y, x):
        my, mx = self.screen.getmaxyx()
        if y >= 0 and y < my - 1 and x >= 0 and x < mx:
            self.screen.move(y, x)

    

class InputBar:
    input_text = ""

    def __init__(self, stdscr):
        curses.noecho()
        stdscr.keypad(True)

    def render(self, stdscr):
        my, mx = stdscr.getmaxyx()
        curses.curs_set(1)
        stdscr.addstr(my-3, 0, "#" * (mx-1))
        stdscr.addstr(my-2, 1, self.input_text)
        stdscr.move(my-2, len(self.input_text)+1)
    
    def handle_input(self, char):
        if len(char) > 1:
            if "KEY_BACKSPACE" == char:
                self.input_text = self.input_text[:-1]
        elif char != "\n":
            self.input_text += char
    
    def get_current_input(self):
        return self.input_text

    def set_current_input(self, txt):
        self.input_text = txt

class MenuWindow:
    items = []
    selected = 0
    indexer = "name"
    msg = "Please select an item: "
    max_items = len(items)
    enter_detected = False

    def __init__(self, stdscr):
        curses.noecho()
        stdscr.keypad(True)

    def set_message(self, new_msg):
        self.msg = new_msg
    
    def set_items(self, new_items, ind = "name"):
        self.items = new_items
        self.indexer = ind

    def was_enter_hit(self):
        return self.enter_detected

    def get_selected(self):
        return self.items[self.selected]

    def render(self, stdscr):
        my, mx = stdscr.getmaxyx()
        self.max_items = min([len(self.items), my-7])
        stdscr.addstr(2, 2, self.msg)
        for i in range(0, self.max_items):
            if i == self.selected:
                stdscr.addstr(3+i, 3, "> " + self.items[i][self.indexer])
            else:
                stdscr.addstr(3+i, 3, self.items[i][self.indexer])
    
    def handle_input(self, char):
        self.enter_detected = False
        if len(char) > 1:
            if "KEY_UP" == char and self.selected > 0:
                self.selected -= 1
            elif "KEY_DOWN" == char and self.selected < self.max_items - 1:
                self.selected += 1
            elif "KEY_ENTER" == char:
                self.enter_detected = True
        elif char == "\n":
            self.enter_detected = True

class SelectionWindow:
    items = []
    selected = 0
    chosen = []
    limit = 0
    msg = "Select by using right arrow, and left to remove:"
    indexer = "name"

    def __init__(self, stdscr):
        curses.noecho()
        stdscr.keypad(True)
        self.chosen = []

    def set_limit(self, mx):
        self.limit = mx

    def set_message(self, message):
        self.msg = message

    def set_items(self, new_items, ind = "name"):
        self.items = new_items
        self.indexer = ind

    def was_enter_hit(self):
        return self.enter_detected

    def get_chosen(self):
        return [self.items[i] for i in range(0, len(self.items)) if i in self.chosen]

    def render(self, stdscr):
        my, mx = stdscr.getmaxyx()
        self.max_items = min([len(self.items), my-7])
        stdscr.addstr(2, 2, self.msg)
        for i in range(0, self.max_items):
            appendable = " [ ]"
            if i in self.chosen:
                appendable = " [x]"
            if i == self.selected:
                stdscr.addstr(3+i, 3, "> " + self.items[i][self.indexer] + appendable)
            else:
                stdscr.addstr(3+i, 3, self.items[i][self.indexer] + appendable)
    
    def handle_input(self, char):
        self.enter_detected = False
        if len(char) > 1:
            if "KEY_UP" == char and self.selected > 0:
                self.selected -= 1
            elif "KEY_DOWN" == char and self.selected < self.max_items - 1:
                self.selected += 1
            elif (self.limit != 0 and self.limit > len(self.chosen)) or self.limit == 0:
                if "KEY_RIGHT" == char and not self.selected in self.chosen:
                    self.chosen.append(self.selected)
                elif "KEY_LEFT" == char and self.selected in self.chosen:
                    self.chosen.remove(self.selected)
            elif "KEY_ENTER" == char:
                self.enter_detected = True
        elif char == "\n":
            self.enter_detected = True


def split_sentence(txt, max_length):
    if len(txt) < max_length:
        return [txt]
    paragraphs = txt.split("\n")
    sentences = []
    for paragraph in paragraphs:
        words = paragraph.rstrip().split(" ")
        sentence = ""
        for i in range(0, len(words)):
            append_now = False
            if len(sentence) + len(words[i]) + 1 < max_length:
                sentence += words[i] + " "
            else:
                append_now = True
            if len(words) - 1 == i or append_now:
                sentences.append(sentence)
                sentence = ""

        sentences.append(sentence)
    return sentences

class DictWindow:
    key_id_pairs = []
    dict_item = {}
    backspace_hit = False
    enter_hit = False

    def __init__(self, key_id):
        self.key_id_pairs = key_id
    
    def set_listing_order(self, key_id):
        self.key_id_pairs = key_id

    def render(self, stdscr, enable_cursor = False):
        stdscr.refresh(enable_cursor)
        for i in range(0, len(self.key_id_pairs)):
            my, mx = stdscr.getmaxyx()
            sentences = split_sentence(str(self.dict_item[self.key_id_pairs[i][0]]), mx - 4)
            if len(sentences) == 1 and len(sentences[0]) < mx - 6 - len(self.key_id_pairs[i][1]):
                stdscr.addstr(2 + (i * 2), 2, self.key_id_pairs[i][1] + ": " + sentences[0])
            else:
                stdscr.addstr(2 + (i * 2), 2, self.key_id_pairs[i][1] + ": ")
                for j in range(0, len(sentences)):
                    if 3 + (i * 2) + j < my - 5:
                        stdscr.addstr(3 + (i * 2) + j, 2, sentences[j])
                    elif 3 + (i * 2) + j == my - 5:
                        stdscr.addstr(3 + (i * 2) + j, 2, "...Expand for more...")
    
    def set_item_to_render(self, item):
        self.dict_item = item
    
    def was_backspace_hit(self):
        return self.backspace_hit

    def was_enter_hit(self):
        return self.enter_hit

    def handle_input(self, char):
        self.enter_hit = False
        if len(char) > 1:
            if "KEY_BACKSPACE" == char:
                self.backspace_hit = True
            elif "KEY_ENTER" == char:
                self.enter_hit = True
        elif char == "\n":
            self.enter_hit = True
    
class Slider:
    min_value = 0
    max_value = 0
    current_value = 0
    pos_x = 0
    pos_y = 0

    def __init__(self, y, x):
        self.pos_x = x
        self.pos_y = y
    
    def set_range(self, mn, mx):
        self.min_value = mn
        self.max_value = mx
    
    def set_current_value(self, current):
        self.current_value = current
    
    def value(self):
        return self.current_value

    def render(self, stdscr, focus = False, y = None, x = None):
        renderable = ""
        renderable += "  " if self.min_value == self.current_value else "< "
        renderable += str(self.current_value)
        renderable += "  " if self.max_value == self.current_value else " >"
        x = x if x is not None else self.pos_x
        y = y if y is not None else self.pos_y
        if focus:
            stdscr.addstr(y, x, renderable, curses.A_REVERSE)
        else:
            stdscr.addstr(y, x, renderable)
    def handle_input(self, char):
        if len(char) > 1:
            if "KEY_LEFT" == char and self.current_value > self.min_value:
                self.current_value -= 1
            elif "KEY_RIGHT" == char and self.current_value < self.max_value:
                self.current_value += 1

class SliderSet:
    sliders = {}
    names = []
    top_x = 0
    top_y = 0
    focused = 0
    def __init__(self, y, x):
        self.top_x = x
        self.top_y = y
        self.names = []
        self.sliders = {}

    def add_slider(self, name):
        slider = Slider(0, 0)
        self.sliders[name] = slider
        self.names.append(name)

    def get_slider(self, name):
        return self.sliders[name]

    def render(self, stdscr):
        i = 0
        for name, slider in self.sliders.items():
            #render message
            stdscr.addstr(self.top_y + (i * 2), self.top_x, name + ": ")
            slider.render(stdscr, i == self.focused, self.top_y + 1 + (i * 2), self.top_x + 2)
            i += 1

    def handle_input(self, char):
        if len(char) > 1:
            if "KEY_UP" == char and self.focused > 0:
                self.focused -= 1
            elif "KEY_DOWN" == char and self.focused < len(self.names) - 1:
                self.focused += 1
            else:
                self.sliders[self.names[self.focused]].handle_input(char)

class MultiDictWindow:
    dict_items = []
    current = 0
    key_id_pairs = []
    backspace_hit = False
    def __init__(self, items):
        self.dict_items = items
        self.current = 0
        self.key_id_pairs = []
    
    def set_listing_order(self, key_id):
        self.key_id_pairs = key_id

    def render(self, stdscr):
        dict_window = DictWindow(self.key_id_pairs)
        dict_window.set_item_to_render(self.dict_items[self.current])
        dict_window.render(stdscr)
    
    def was_backspace_hit(self):
        return self.backspace_hit

    def handle_input(self, char):
        self.backspace_hit = False
        if len(char) > 1:
            if char == "KEY_LEFT" and self.current > 0:
                self.current -= 1
            elif char == "KEY_RIGHT" and self.current < len(self.dict_items) - 1:
                self.current += 1
            elif "KEY_BACKSPACE" == char:
                self.backspace_hit = True
                