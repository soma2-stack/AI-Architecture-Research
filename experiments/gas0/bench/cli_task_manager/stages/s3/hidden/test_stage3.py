from taskapp.model import Task
from taskapp.projects import ProjectRegistry, project_tasks
from taskapp.store import TaskStore

def test_tie_breaker_is_due_date_then_task_id():
    registry=ProjectRegistry(); registry.add("p","P")
    rows=[Task("z","Z",due_date="2025-12-31",project_id="p"),
          Task("a","A",due_date="2025-12-31",project_id="p")]
    assert [r.task_id for r in project_tasks(rows,"p","2026-01-01")] == ["a","z"]

def test_projects_round_trip_with_task_association(tmp_path):
    store=TaskStore(tmp_path/"tasks.json"); store.projects={"p":"Home"}
    store.add(Task("a","A",project_id="p")); store.save()
    loaded=TaskStore.load(store.path)
    assert loaded.projects=={"p":"Home"}
    assert loaded.tasks[0].project_id=="p"
