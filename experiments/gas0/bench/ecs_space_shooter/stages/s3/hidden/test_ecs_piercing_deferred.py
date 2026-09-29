import importlib.util

def test_piercing_is_deferred():
    assert importlib.util.find_spec("spaceecs.piercing") is None
