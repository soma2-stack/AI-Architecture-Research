from expr import evaluate

def test_deferred_boolean_operators_now_short_circuit():
    assert evaluate("0 and unknown(1)")==0
    assert evaluate("1 or unknown(1)")==1
