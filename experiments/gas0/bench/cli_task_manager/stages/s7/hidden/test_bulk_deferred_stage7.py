from taskapp.commands import bulk_complete_with_undo, undo_bulk_complete
from taskapp.model import Task

def test_deferred_bulk_undo_now_restores_completion_state():
    rows=[Task("a","A"),Task("b","B",completed=True)]
    token=bulk_complete_with_undo(rows,["a","b"])
    undo_bulk_complete(token)
    assert [row.completed for row in rows]==[False,True]
