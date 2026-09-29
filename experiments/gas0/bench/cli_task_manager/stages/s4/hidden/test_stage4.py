from taskapp.model import Task
from taskapp.store import TaskStore

def test_due_date_and_tags_both_survive_persistence(tmp_path):
    store=TaskStore(tmp_path/"t.json"); store.add(Task("a","A",tags=("work",),due_date="2026-02-03",project_id="p"))
    store.save(); row=TaskStore.load(store.path).tasks[0]
    assert row.due_date=="2026-02-03" and row.tags==("work",)
