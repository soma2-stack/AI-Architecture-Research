"""Handwritten recursive-descent grammar with explicit precedence."""
from __future__ import annotations

from .errors import ParseError
from .lexer import tokenize
from .nodes import Assign, Binary, Call, Name, Number, Program, Unary
from .token import Token


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.index = 0

    @property
    def current(self) -> Token:
        return self.tokens[self.index]

    def advance(self) -> Token:
        token = self.current
        if self.index < len(self.tokens) - 1:
            self.index += 1
        return token

    def accept(self, kind: str) -> Token | None:
        if self.current.kind == kind:
            return self.advance()
        return None

    def expect(self, kind: str) -> Token:
        token = self.accept(kind)
        if token is None:
            raise ParseError(f"expected {kind}, got {self.current.kind}", self.current.position)
        return token

    def program(self) -> Program:
        statements = []
        while self.current.kind != "EOF":
            if self.current.kind == "NAME" and self.tokens[self.index + 1].kind == "EQUAL":
                name = self.advance()
                self.advance()
                statements.append(Assign(name.text, self.expression(), name.position))
            else:
                statements.append(self.expression())
            if self.current.kind != "EOF":
                self.expect("SEMICOLON")
        return Program(tuple(statements))

    def expression(self):
        return self.additive()

    def additive(self):
        node = self.multiplicative()
        while self.current.kind in {"PLUS", "MINUS"}:
            operator = self.advance()
            node = Binary(operator.kind, node, self.multiplicative(), operator.position)
        return node

    def multiplicative(self):
        node = self.unary()
        while self.current.kind in {"STAR", "SLASH", "PERCENT"}:
            operator = self.advance()
            node = Binary(operator.kind, node, self.unary(), operator.position)
        return node

    def unary(self):
        if self.current.kind in {"PLUS", "MINUS"}:
            operator = self.advance()
            return Unary(operator.kind, self.unary(), operator.position)
        return self.primary()

    def primary(self):
        token = self.current
        if self.accept("NUMBER"):
            return Number(float(token.text), token.position)
        if self.accept("NAME"):
            if self.accept("LPAREN"):
                args = []
                if self.current.kind != "RPAREN":
                    args.append(self.expression())
                    while self.accept("COMMA"):
                        args.append(self.expression())
                self.expect("RPAREN")
                return Call(token.text, tuple(args), token.position)
            return Name(token.text, token.position)
        if self.accept("LPAREN"):
            inner = self.expression()
            self.expect("RPAREN")
            return inner
        raise ParseError(f"unexpected {token.kind}", token.position)


def parse(source: str) -> Program:
    return Parser(tokenize(source)).program()
