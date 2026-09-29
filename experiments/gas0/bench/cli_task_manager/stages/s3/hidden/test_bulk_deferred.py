def test_bulk_complete_with_undo_is_deferred():
    from taskapp import commands
    assert not hasattr(commands,"bulk_complete_with_undo")
