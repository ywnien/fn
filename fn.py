#!/usr/bin/env python
import json

from prompt_toolkit.application import Application
from prompt_toolkit.filters import Condition
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import (ConditionalContainer, HSplit,
                                              VSplit, Window)
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.dimension import LayoutDimension as D
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import SearchToolbar, TextArea

from fn.lexer import NumLexer


# Load or create bookmark
try:
    with open("json/bookmark.json", "r") as f:
        bookmark = json.load(f)
except FileNotFoundError:
    bookmark = {
        "book": 0,
        "chapter": 0,
    }
    with open("json/bookmark.json", "w") as f:
        json.dump(bookmark, f, indent=4)

# Read bible
with open("json/CUV.json", "r") as f:
    cuv = json.load(f)


class Reading:
    def __init__(self, bookmark=bookmark, bible=cuv):
        self._book = bookmark["book"]
        self._chapter = bookmark["chapter"]
        self._book_name_list = list(bible)
        self._chapter_max_list = [len(bible[name]) - 1 for name in list(bible)]
        
        self._text_list = bible[self.book][self.chapter]
        self.text = "\n".join(self._text_list)
    
    def update(self, bible=cuv):
        self._text_list = bible[self.book][self.chapter]
        self.text = "\n".join(self._text_list)

    @property
    def book(self):
        return self._book_name_list[self._book]
    
    @property
    def chapter(self):
        return str(self._chapter)

    def next_book(self):
        if self._book == 65:
            self._book = 0
        else:
            self._book += 1
        self._chapter = 1

        self.update()

    def previous_book(self):
        if self._book == 0:
            self._book = 65
        else:
            self._book -= 1
        self._chapter = 1

        self.update()

    def next_chapter(self):
        if self._chapter == self._chapter_max_list[self._book]:
            self._chapter = 1
        else:
            self._chapter += 1
            
        self.update()

    def previous_chapter(self):
        if self._chapter == 1:
            self._chapter = self._chapter_max_list[self._book]
        else:
            self._chapter -= 1

        self.update()
    

now = Reading()


class Switch:
    memory_system = False


@Condition
def scripture_filter():
    return Switch.scripture

@Condition
def memory_system_filter():
    return Switch.memory_system

search_bar = SearchToolbar()

scripture = TextArea(
        text=now.text,
        read_only=True,
        scrollbar=True,
        search_field=search_bar,
        focus_on_click=True,
        lexer=NumLexer(),
        width=D(weight=4)
)

"""
TODO: build another TextArea-like container but can receive `filter`.
"""
memory_system = ConditionalContainer(
    content=TextArea(
        text="",
        read_only=False,
        scrollbar=True,
        search_field=search_bar,
        #lexer=NumLexer(),
        width=D(weight=1)
    ),
    filter=memory_system_filter
)

body = VSplit(
    [scripture, memory_system]
)


def status():
    return [
        ("class:status", f"{now.book} - "),
        ("class:status", now.chapter),
        ("class:status", " - Press "),
        ("class:status.key", "q"),
        ("class:status", " to exit, "),
        ("class:status.key", "/"),
        ("class:status", " for searching, "),
        ("class:status.key", "Ctrl-Up/Down"),
        ("class:status", " to change chapter, "),
        ("class:status.key", "Ctrl-Left/Right"),
        ("class:status", " to change book."),
    ]


"""
TODO: Wrap root_container with Menucontainer
and add Menu objects to navigate to each book.
"""
root_container = HSplit(
    [
        Window(
            content=FormattedTextControl(status),
            height=D.exact(1),
            style="class:status",
        ),
        body,
        search_bar,
    ]
)


kb = KeyBindings()

@kb.add("c-c")
@kb.add("q")
def _(event):
    "Quit."
    event.app.exit()

@kb.add("tab")
def _(event):
    event.app.layout.focus_next()

@kb.add("s-tab")
def _(event):
    event.app.layout.focus_previous()

@kb.add("c-up")
def _(_):
    now.previous_chapter()
    scripture.text = now.text

@kb.add("c-down")
def _(_):
    now.next_chapter()
    scripture.text = now.text

@kb.add("c-left")
def _(_):
    now.previous_book()
    scripture.text = now.text

@kb.add("c-right")
def _(_):
    now.next_book()
    scripture.text = now.text

@kb.add("f1")
@kb.add("c-j")
def _(event):
    Switch.memory_system = not Switch.memory_system
    

style = Style.from_dict(
    {
        "status": "reverse",
        "status.key": "#62A8AC",
    }
)

application = Application(
    layout=Layout(root_container, focused_element=scripture),
    key_bindings=kb,
    enable_page_navigation_bindings=True,
    mouse_support=True,
    style=style,
    full_screen=True,
)


def main():
    application.run()

    bookmark["book"] = now._book
    bookmark["chapter"] = now._chapter

    with open("json/bookmark.json", "w") as f:
        json.dump(bookmark, f, indent=4)


if __name__ == "__main__":
    main()