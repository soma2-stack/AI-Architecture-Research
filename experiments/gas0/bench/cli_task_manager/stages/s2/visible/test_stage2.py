from taskapp.model import Task
from taskapp.query import list_tasks

def test_default_hides_completed_tasks():
    rows=[Task("a","A",completed=True),Task("b","B")]
    assert [task.task_id for task in list_tasks(rows)]==["b"]

def test_explicit_flag_restores_completed_rows():
    rows=[Task("a","A",completed=True),Task("b","B")]
    assert [task.task_id for task in list_tasks(rows,include_done=True)]==["b","a"]
