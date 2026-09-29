from taskapp.commands import bulk_complete_with_undo, undo_bulk_complete
from taskapp.model import Task

def test_bulk_completion_undo_restores_mixed_prior_state():
    rows=[Task("a","A"),Task("b","B",completed=True)]
    token=bulk_complete_with_undo(rows,["a","b"])
    assert all(row.completed for row in rows)
    assert undo_bulk_complete(token)==2
    assert [row.completed for row in rows]==[False,True]
