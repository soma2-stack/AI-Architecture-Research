import pytest
from taskapp.commands import add_task, complete_task, reopen_task, update_title
from taskapp.errors import MissingTask, ValidationError
from taskapp.model import Task
from taskapp.query import list_tasks, search_title, count_open, count_by_tag


def sample():
    return [Task("t2", "Write tests", tags=("work",)),
            Task("t1", "Buy milk", completed=True, tags=("home", "errand"))]


def test_task_normalizes_title_and_tags():
    task = Task(" t1 ", "  Buy   milk ", tags=("Home", "home", " errand "))
    assert task.title == "Buy milk"
    assert task.tags == ("errand", "home")


def test_task_requires_identity_and_title():
    with pytest.raises(ValidationError):
        Task("", "valid")
    with pytest.raises(ValidationError):
        Task("t1", "  ")


def test_add_and_duplicate_rejected():
    rows=[]
    assert add_task(rows,"t1","First").title == "First"
    with pytest.raises(ValidationError):
        add_task(rows,"t1","Duplicate")


def test_completion_and_reopen_are_repeatable():
    rows=sample()
    assert complete_task(rows,"t2").completed is True
    assert complete_task(rows,"t2").completed is True
    assert reopen_task(rows,"t2").completed is False


def test_missing_task_mutation_is_specific_error():
    with pytest.raises(MissingTask):
        complete_task([],"missing")


def test_title_update_trims_and_validates():
    rows=sample()
    assert update_title(rows,"t2"," Revised title ").title == "Revised title"
    with pytest.raises(ValidationError):
        update_title(rows,"t2"," ")


def test_listing_is_stable_and_open_first():
    assert [r.task_id for r in list_tasks(sample())] == ["t2","t1"]


def test_search_is_case_insensitive_and_empty_safe():
    rows=sample()
    assert [r.task_id for r in search_title(rows,"BUY")] == ["t1"]
    assert search_title(rows,"   ") == []


def test_open_and_tag_counts():
    rows=sample()
    assert count_open(rows)==1
    assert count_by_tag(rows)=={"errand":1,"home":1,"work":1}


def test_completed_filter_can_be_requested_explicitly():
    assert [r.task_id for r in list_tasks(sample(),include_done=False)]==["t2"]
