from taskapp.cli import dispatch
from taskapp.model import Task
from taskapp.store import TaskStore

def test_all_fields_survive_integrated_save_load(tmp_path):
    store=TaskStore(tmp_path/"t.json"); store.projects={"p":"Work"}
    store.add(Task("a","Review",tags=("work",),due_date="2026-04-05",project_id="p",status="in_progress"))
    store.save(); loaded=TaskStore.load(store.path)
    row=loaded.tasks[0]
    assert (row.tags,row.due_date,row.project_id,row.status)==(("work",),"2026-04-05","p","in_progress")

def test_tag_filter_and_project_sort_compose_without_extra_tasks(tmp_path):
    store=TaskStore(tmp_path/"t.json"); store.projects={"p":"P"}
    store.add(Task("a","Late",tags=("work",),due_date="2026-03-01",project_id="p"))
    store.add(Task("b","Other",tags=("home",),due_date="2026-02-01",project_id="p"))
    output=dispatch(store,["list","--tag","work","--project","p","--today","2026-03-02"])
    assert "a: Late" in output and "b: Other" not in output
