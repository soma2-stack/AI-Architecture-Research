"""Lexer tokens and punctuation set."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Token:
    kind: str
    text: str
    position: int

    def __str__(self):
        return f"{self.kind}({self.text})@{self.position}"


PUNCTUATION = {
    "+": "PLUS", "-": "MINUS", "*": "STAR", "/": "SLASH",
    "%": "PERCENT", "(": "LPAREN", ")": "RPAREN",
    "=": "EQUAL", ",": "COMMA", ";": "SEMICOLON",
}
