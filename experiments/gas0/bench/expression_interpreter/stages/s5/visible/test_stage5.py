import pytest
from expr import evaluate
from expr.errors import EvalError

def test_true_and_floor_division_are_distinct():
    assert evaluate("7/2") == 3.5
    assert evaluate("7//2") == 3

def test_negative_floor_rounds_down():
    assert evaluate("-7//2") == -4

def test_zero_divisor_is_a_language_error():
    with pytest.raises(EvalError,match="division by zero"):
        evaluate("1//0")
