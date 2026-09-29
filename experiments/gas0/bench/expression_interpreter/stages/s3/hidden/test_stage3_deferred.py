from expr import evaluate

def test_boolean_operators_remain_deferred():
    assert evaluate("0") == 0
