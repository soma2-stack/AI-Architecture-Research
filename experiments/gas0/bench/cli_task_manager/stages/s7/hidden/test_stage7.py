from taskapp.commands import bulk_complete_with_undo, undo_bulk_complete
from taskapp.model import Task
from taskapp.store import TaskStore

def test_legacy_save_missing_or_null_projects_loads_empty_registry():
    payload={"version":1,"tasks":[],"preferences":{},"projects":None}
    assert TaskStore.from_payload("unused",payload).projects=={}

def test_bulk_undo_does_not_reorder_or_change_unselected_tasks():
    rows=[Task("a","A"),Task("b","B",completed=True),Task("c","C")]
    token=bulk_complete_with_undo(rows,["c","a"])
    undo_bulk_complete(token)
    assert [row.task_id for row in rows]==["a","b","c"]
    assert [row.completed for row in rows]==[False,True,False]
