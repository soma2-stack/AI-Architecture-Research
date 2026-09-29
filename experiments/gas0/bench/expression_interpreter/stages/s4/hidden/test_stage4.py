from expr import evaluate

def test_ceil_arity_fix_preserves_other_unary_builtins():
    assert evaluate("floor(3.8)") == 3
    assert evaluate("ceil(3.2)") == 4
    assert evaluate("abs(-5.5)") == 5.5
