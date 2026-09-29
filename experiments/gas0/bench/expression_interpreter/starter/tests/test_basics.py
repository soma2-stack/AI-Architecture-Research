import pytest

from expr import Environment, evaluate
from expr.errors import EvalError, LexError, ParseError
from expr.lexer import tokenize
from expr.nodes import Binary, Number
from expr.parser import parse


def test_lex_positions():
    assert [(t.kind, t.position) for t in tokenize("a+12")][:3] == [
        ("NAME", 0), ("PLUS", 1), ("NUMBER", 2)]


def test_lex_comment():
    assert [t.kind for t in tokenize("1 #ignored\n+2")] == ["NUMBER", "PLUS", "NUMBER", "EOF"]


def test_lex_invalid():
    with pytest.raises(LexError):
        tokenize("1 @ 2")


def test_parser_precedence():
    tree = parse("2+3*4").statements[0]
    assert isinstance(tree, Binary)
    assert isinstance(tree.right, Binary)


def test_parser_parentheses():
    assert evaluate("(2+3)*4") == 20


def test_arithmetic():
    assert evaluate("8/2+5%3") == 6


def test_unary():
    assert evaluate("-3*2") == -6


def test_decimal():
    assert evaluate("0.5+1.25") == 1.75


def test_assignment_and_lookup():
    env = Environment()
    assert evaluate("a=3; a*4", env) == 12
    assert env.snapshot() == {"a": 3.0}


def test_unknown_variable():
    with pytest.raises(EvalError, match="undefined variable"):
        evaluate("missing+1")


def test_division_by_zero():
    with pytest.raises(EvalError, match="division by zero"):
        evaluate("1/0")


def test_incomplete_expression():
    with pytest.raises(ParseError):
        evaluate("1+")


def test_builtin_mean():
    assert evaluate("mean(2,4,6)") == 4


def test_builtin_nested():
    assert evaluate("max(1, min(5,3))") == 3
