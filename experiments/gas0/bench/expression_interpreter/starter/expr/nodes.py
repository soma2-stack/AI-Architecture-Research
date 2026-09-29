"""Interpreter syntax tree. Nodes carry precise positions for diagnostics."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Number:
    value: float
    position: int


@dataclass(frozen=True)
class Name:
    identifier: str
    position: int


@dataclass(frozen=True)
class Unary:
    operator: str
    operand: object
    position: int


@dataclass(frozen=True)
class Binary:
    operator: str
    left: object
    right: object
    position: int


@dataclass(frozen=True)
class Assign:
    identifier: str
    value: object
    position: int


@dataclass(frozen=True)
class Call:
    callee: str
    arguments: tuple[object, ...]
    position: int


@dataclass(frozen=True)
class Program:
    statements: tuple[object, ...]


EXPRESSION_NODES = (Number, Name, Unary, Binary, Call)
