from expr import evaluate

def test_ceil_accepts_one_argument():
    assert evaluate("ceil(3.2)") == 4
