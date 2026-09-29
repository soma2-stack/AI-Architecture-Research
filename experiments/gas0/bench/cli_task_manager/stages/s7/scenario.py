from taskapp.store import TaskStore
legacy={"version":1,"tasks":[{"task_id":"a","title":"Old"}],"preferences":{},"projects":None}
store=TaskStore.from_payload("unused",legacy)
assert store.projects=={}
