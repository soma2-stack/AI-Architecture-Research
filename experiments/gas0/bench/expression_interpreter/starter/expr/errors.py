"""Stable errors with source offsets for command-line consumers."""


class ExpressionError(Exception):
    def __init__(self, message: str, position: int | None = None):
        self.message = message
        self.position = position
        suffix = "" if position is None else f" at position {position}"
        super().__init__(message + suffix)


class LexError(ExpressionError):
    pass


class ParseError(ExpressionError):
    pass


class EvalError(ExpressionError):
    pass
