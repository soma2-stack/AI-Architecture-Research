def test_cleansing_charm_is_deferred():
    import rogue.effects as effects
    assert not hasattr(effects,"use_cleansing_charm")
