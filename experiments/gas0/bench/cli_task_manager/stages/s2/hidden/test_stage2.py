from taskapp.model import Task
from taskapp.query import list_tasks

def test_tag_filter_does_not_reintroduce_completed_tasks():
    rows=[Task("a","A",completed=True,tags=("work",)),Task("b","B",tags=("work",))]
    assert [task.task_id for task in list_tasks(rows,tag="work")]==["b"]

def test_explicit_tag_query_can_show_done_rows():
    rows=[Task("a","A",completed=True,tags=("work",))]
    assert [task.task_id for task in list_tasks(rows,tag="work",include_done=True)]==["a"]
