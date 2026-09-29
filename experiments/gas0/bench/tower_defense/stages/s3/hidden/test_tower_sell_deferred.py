def test_tower_selling_is_deferred():
    import td.economy as economy
    assert not hasattr(economy, "sell_tower")
