"""Explicit character scanner, with no host-language eval or regex parser."""
from __future__ import annotations

from .errors import LexError
from .token import PUNCTUATION, Token


def tokenize(source: str) -> list[Token]:
    tokens = []
    cursor = 0
    while cursor < len(source):
        start = cursor
        char = source[cursor]
        if char.isspace():
            cursor += 1
            continue
        if char == "#":
            while cursor < len(source) and source[cursor] != "\n":
                cursor += 1
            continue
        if char in PUNCTUATION:
            tokens.append(Token(PUNCTUATION[char], char, cursor))
            cursor += 1
            continue
        if char.isdigit():
            while cursor < len(source) and source[cursor].isdigit():
                cursor += 1
            if cursor < len(source) and source[cursor] == ".":
                cursor += 1
                if cursor >= len(source) or not source[cursor].isdigit():
                    raise LexError("decimal point requires digits", cursor)
                while cursor < len(source) and source[cursor].isdigit():
                    cursor += 1
            tokens.append(Token("NUMBER", source[start:cursor], start))
            continue
        if char.isalpha() or char == "_":
            cursor += 1
            while cursor < len(source) and (source[cursor].isalnum() or source[cursor] == "_"):
                cursor += 1
            tokens.append(Token("NAME", source[start:cursor], start))
            continue
        raise LexError(f"unexpected character {char!r}", cursor)
    tokens.append(Token("EOF", "", len(source)))
    return tokens
