import pytest
from expr import evaluate
from expr.errors import EvalError

def test_comparison_precedence_and_numeric_boolean():
    assert evaluate("2 + 3 * 4 == 14") == 1.0
    assert evaluate("2 + 3 * 4 < 15") == 1.0
    assert evaluate("4 != 4") == 0.0

def test_chained_assignment_keeps_comparison_value():
    assert evaluate("ok = 3 >= 3; ok + 2") == 3.0

def test_unlike_scalar_types_are_rejected():
    from expr.nodes import Binary, Number
    from expr.runtime import Environment, evaluate_node
    with pytest.raises(EvalError, match="same type"):
        evaluate_node(Binary("EQ", Number(1, 0), Number(True, 0), 0), Environment())
