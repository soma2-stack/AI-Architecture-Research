import pytest
from expr import evaluate
from expr.errors import EvalError

def test_relational_operators_and_parenthesized_boolean():
    assert evaluate("(5 >= 5) * 10 + (3 < 1)") == 10
    assert evaluate("7 <= 7") == 1
    assert evaluate("9 > 10") == 0

def test_assignment_does_not_coerce_boolean_to_python_bool():
    from expr import Environment
    env=Environment(); evaluate("flag = 1 == 1",env)
    assert env.lookup("flag") == 1.0 and type(env.lookup("flag")) is float

def test_equality_is_not_truthiness():
    assert evaluate("2 == 1") == 0
