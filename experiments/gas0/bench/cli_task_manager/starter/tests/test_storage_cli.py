import json
import pytest
from taskapp.cli import dispatch
from taskapp.errors import StorageError
from taskapp.model import Task
from taskapp.store import TaskStore


def test_store_round_trip_preserves_fields(tmp_path):
    path=tmp_path/"tasks.json"; store=TaskStore(path)
    store.add(Task("t1","Plan",description="one",tags=("work",),due_date="2026-03-01"))
    store.save(); loaded=TaskStore.load(path)
    assert loaded.tasks[0].to_dict()==store.tasks[0].to_dict()


def test_missing_file_creates_empty_store(tmp_path):
    store=TaskStore.load(tmp_path/"missing.json")
    assert store.tasks==[]


def test_bad_json_is_reported(tmp_path):
    path=tmp_path/"bad.json"; path.write_text("{")
    with pytest.raises(StorageError): TaskStore.load(path)


def test_unknown_schema_is_rejected(tmp_path):
    with pytest.raises(StorageError):
        TaskStore.from_payload(tmp_path/"x",{"version":9,"tasks":[]})


def test_duplicate_ids_are_rejected_on_load(tmp_path):
    payload={"version":1,"tasks":[{"task_id":"a","title":"A"},{"task_id":"a","title":"B"}]}
    with pytest.raises(StorageError): TaskStore.from_payload(tmp_path/"x",payload)


def test_store_remove_is_idempotent_for_missing_id(tmp_path):
    store=TaskStore(tmp_path/"x")
    assert not store.remove("x")


def test_cli_add_done_list_cycle(tmp_path):
    store=TaskStore(tmp_path/"tasks.json")
    assert dispatch(store,["add","t1","Write tests"])=="t1"
    assert dispatch(store,["done","t1"])=="done"
    assert "[x] t1" in dispatch(store,["list"])


def test_cli_summary_and_unknown_errors(tmp_path):
    store=TaskStore(tmp_path/"tasks.json")
    assert dispatch(store,["summary"])=="0/0 complete; 0 open"
    assert dispatch(store,["done","missing"]).startswith("error:")


def test_json_payload_is_deterministic(tmp_path):
    store=TaskStore(tmp_path/"x"); store.add(Task("a","A"))
    assert json.dumps(store.payload(),sort_keys=True)==json.dumps(store.payload(),sort_keys=True)


def test_store_preferences_are_copied(tmp_path):
    store=TaskStore(tmp_path/"x"); payload=store.payload()
    payload["preferences"]["hide_done"]=True
    assert store.preferences["hide_done"] is False
