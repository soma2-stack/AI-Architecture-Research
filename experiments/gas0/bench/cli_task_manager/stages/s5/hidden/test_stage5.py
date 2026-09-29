from taskapp.store import TaskStore

def test_v1_migration_preserves_done_and_open_tasks(tmp_path):
    old={"version":1,"tasks":[{"task_id":"a","title":"A","completed":True},
                                 {"task_id":"b","title":"B","completed":False}]}
    store=TaskStore.from_payload(tmp_path/"old.json",old)
    assert [(row.task_id,row.status) for row in store.tasks]==[("a","done"),("b","open")]
    store.save(); assert all("status" in row for row in store.payload()["tasks"])

def test_in_progress_is_not_reported_complete():
    from taskapp.model import Task
    row=Task("a","A",status="in_progress")
    assert row.completed is False
