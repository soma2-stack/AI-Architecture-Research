import pytest
from expr import evaluate
from expr.errors import EvalError

def test_wrong_user_function_arity_is_language_error():
    with pytest.raises(EvalError,match="wrong number"):
        evaluate("fn one(x)=x; one()")

def test_short_circuit_skips_undefined_calls():
    assert evaluate("0 and missing(1)") == 0
    assert evaluate("1 or missing(2)") == 1
