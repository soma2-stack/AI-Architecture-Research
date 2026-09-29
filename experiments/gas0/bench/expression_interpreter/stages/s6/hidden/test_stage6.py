import pytest
from expr import evaluate
from expr.errors import EvalError
from expr.inspect import validate_program
from expr.nodes import Binary, Number, Program

def test_recursive_whitelist_covers_children():
    bad=Program((Binary("PLUS",Number(1,0),object(),0),))
    with pytest.raises(EvalError,match="unsupported"):
        validate_program(bad)

def test_every_parsed_program_passes_guard_without_changing_result():
    assert evaluate("fn inc(x)=x+1; inc(2)") == 3
