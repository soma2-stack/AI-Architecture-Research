def test_legacy_boolean_save_contract():
    from taskapp.store import TaskStore
    from taskapp.model import Task
    store=TaskStore("unused"); store.add(Task("a","A",completed=True))
    assert store.payload()["tasks"][0]["completed"] is True
