import pytest
from expr.errors import EvalError
from expr.inspect import validate_program
from expr.nodes import Program

def test_unknown_ast_nodes_are_rejected():
    with pytest.raises(EvalError,match="unsupported"):
        validate_program(Program((object(),)))
