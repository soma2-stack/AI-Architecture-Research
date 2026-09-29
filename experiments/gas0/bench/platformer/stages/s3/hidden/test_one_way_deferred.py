def test_one_way_platform_support_is_deferred():
    import importlib.util
    assert importlib.util.find_spec("platformer.one_way") is None
