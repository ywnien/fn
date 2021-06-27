#!/usr/bin/env python
"""
Only digits are painted dark gray.

ref: https://github.com/prompt-toolkit/python-prompt-toolkit/blob/master/examples/prompts/custom-lexer.py
"""
from prompt_toolkit.lexers import Lexer
from prompt_toolkit.shortcuts import prompt


class NumLexer(Lexer):
    def lex_document(self, document):
        colors = {True: "#626262", False: ""}

        def get_line(lineno):
            return [
                (colors[char.isdigit()], char)
                for char in document.lines[lineno]
            ]

        return get_line