"""Formatting values and short, stable diagnostics."""
from __future__ import annotations

from .errors import ExpressionError


def number(value: float | None) -> str:
    if value is None:
        return ""
    if value == int(value):
        return str(int(value))
    return format(value, ".12g")


def diagnostic(source: str, error: ExpressionError) -> str:
    if error.position is None:
        return str(error)
    position = min(max(error.position, 0), len(source))
    line_start = source.rfind("\n", 0, position) + 1
    line_end = source.find("\n", position)
    if line_end < 0:
        line_end = len(source)
    line = source[line_start:line_end]
    caret = " " * (position - line_start) + "^"
    return f"{error.message}\n{line}\n{caret}"
