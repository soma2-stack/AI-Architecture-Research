from taskapp.model import Task
from taskapp.store import TaskStore

def test_status_enum_and_compatibility_property():
    row=Task("a","A"); assert row.status=="open"
    row.completed=True; assert row.status=="done" and row.completed

def test_new_payload_uses_status_not_boolean():
    store=TaskStore("unused"); store.add(Task("a","A",completed=True))
    row=store.payload()["tasks"][0]
    assert row["status"]=="done" and "completed" not in row
