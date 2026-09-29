from expr import Environment, evaluate
from expr.errors import EvalError
import pytest

def test_and_or_evaluate_right_side_only_when_needed():
    assert evaluate("0 and unknown") == 0
    assert evaluate("1 or unknown") == 1
    assert evaluate("1 and 5") == 1
    assert evaluate("0 or 8") == 1

def test_evaluated_right_side_normalizes_to_boolean():
    assert evaluate("1 and 4")==1
    assert evaluate("0 or 8")==1

def test_extra_and_missing_arguments_both_rejected():
    for source in ("fn id(x)=x; id()","fn id(x)=x; id(1,2)"):
        with pytest.raises(EvalError,match="wrong number"):
            evaluate(source)
