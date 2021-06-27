#!/usr/bin/env python
"""
This script downloads whole Bible into json/CUV.json,
and also an example showing how to use `Browser` and Menu‵.
"""
import json

from fn.browser import Browser, Menu
from fn.wsl2 import xlaunch


url = "https://www.chinesebible.org.hk/onlinebible/index.php"


def title_parse(titles: list):
    ch_titles = []
    en_titles = []

    for title in titles:
        for i, char in enumerate(title):

            if char == " ":
                ch_titles.append(title[:i])
                en_titles.append(title[i+1:])
                break

    return ch_titles, en_titles


def vision():
    """
    Gets all scriptures. Shall I find my vision sooner or later?
    """
    cuv = {} 

    for i, book in enumerate(books.opts()):
            cuv[ch_titles[i]] = {}
            books.reattach() # Menu(Select) detaches when switches frame.
            books.select(book)
            chapters = Menu(bible.find_one(), "chapter")

            for chapter in chapters.opts():

                if chapter == 0:
                    pass
                else:
                    chapters.reattach()
                    chapters.select(chapter)

                    bible.frame("window2")
                    verses = bible.find("a", "tag")
                    verses = [verse.text for verse in verses if verse.text != ""]
                    cuv[ch_titles[i]][chapter] = verses

                    bible.frame("main_selection")

    return cuv


with xlaunch():
    with Browser(url) as bible:
        bible.frame("main_selection")
        books = Menu(bible.find_one(), "biblebook")

        titles = books.opts(info="text")
        ch_titles, en_titles = title_parse(titles)

        cuv = vision()

with open("json/CUV.json", "w", encoding="utf-8") as f:
    json.dump(cuv, f, indent=4, ensure_ascii=False)