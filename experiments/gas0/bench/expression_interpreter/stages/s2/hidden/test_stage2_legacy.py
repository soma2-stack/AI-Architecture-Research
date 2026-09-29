from expr import evaluate

def test_legacy_integer_division_contract():
    assert evaluate("7/2") == 3
