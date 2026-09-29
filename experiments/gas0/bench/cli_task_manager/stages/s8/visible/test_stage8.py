from taskapp.cli import dispatch
from taskapp.model import Task
from taskapp.store import TaskStore

def test_project_command_and_project_listing(tmp_path):
    store=TaskStore(tmp_path/"t.json"); store.projects={}
    store.add(Task("a","A",tags=("work",),due_date="2025-12-30",project_id="p"))
    assert dispatch(store,["project","p","Work"])=="p"
    assert "a: A" in dispatch(store,["list","--project","p","--tag","work"])

def test_cli_bulk_done_and_undo(tmp_path):
    store=TaskStore(tmp_path/"t.json"); store.add(Task("a","A"))
    assert dispatch(store,["bulk-done","a"])=="done"
    assert store.tasks[0].completed
    assert dispatch(store,["undo"])=="undone" and not store.tasks[0].completed
