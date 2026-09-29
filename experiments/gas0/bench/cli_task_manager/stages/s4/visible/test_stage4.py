from taskapp.model import Task
from taskapp.store import TaskStore

def test_due_date_survives_save_and_reload(tmp_path):
    store=TaskStore(tmp_path/"tasks.json"); store.add(Task("a","A",due_date="2026-02-03",project_id="p"))
    store.save(); assert TaskStore.load(store.path).tasks[0].due_date=="2026-02-03"
