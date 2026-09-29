import pytest
from taskapp.dates import date_sort_key, is_overdue, parse_date
from taskapp.errors import ValidationError
from taskapp.formatting import format_task, format_tasks, format_summary, table_row
from taskapp.model import Task
from taskapp.query import sort_by_due_date
from taskapp.analytics import (completion_ratio, completion_by_tag, daily_load,
                               compact_summary, dashboard, due_between, due_soon,
                               next_due, overdue_tasks, status_counts, tagged_task_ids, tag_counts)


def test_date_parser_accepts_only_iso_calendar_dates():
    assert parse_date("2026-02-28")=="2026-02-28"
    with pytest.raises(ValidationError): parse_date("02/28/2026")
    with pytest.raises(ValidationError): parse_date("2026-02-30")


def test_optional_date_is_empty():
    assert parse_date(None) is None
    assert parse_date("") is None


def test_overdue_is_strictly_before_today():
    assert is_overdue("2026-01-01","2026-01-02")
    assert not is_overdue("2026-01-02","2026-01-02")
    assert not is_overdue(None,"2026-01-02")


def test_date_sort_key_places_missing_last():
    assert date_sort_key(None)>date_sort_key("2026-12-31")


def test_due_sort_uses_task_id_for_ties():
    rows=[Task("b","B",due_date="2026-05-01"),Task("a","A",due_date="2026-05-01")]
    assert [r.task_id for r in sort_by_due_date(rows)]==["a","b"]


def test_format_labels_status_and_tags():
    row=Task("a","Review",tags=("work",),due_date="2026-01-01")
    assert format_task(row)=="[ ] a: Review #work due=2026-01-01"
    assert format_task(row,today="2026-01-02").endswith("overdue")


def test_empty_listing_is_explicit():
    assert format_tasks([])=="(no tasks)"


def test_summary_counts_are_consistent():
    rows=[Task("a","A"),Task("b","B",completed=True)]
    assert format_summary(rows)=="1/2 complete; 1 open"


def test_table_quotes_delimiters_and_newlines():
    row=Task("a","A, B",description="line\nnext")
    assert '"A, B"' in table_row(row)


def test_format_has_no_terminal_escape_sequences():
    assert "\x1b" not in format_task(Task("a","Plain"))


def test_empty_analytics_are_defined():
    assert completion_ratio([])==0.0
    assert tag_counts([])=={}
    assert daily_load([])=={}


def test_completion_ratio_is_fraction_not_percent():
    rows=[Task("a","A",completed=True),Task("b","B")]
    assert completion_ratio(rows)==0.5


def test_due_between_is_inclusive_and_stable():
    rows=[Task("b","B",due_date="2026-03-03"),Task("a","A",due_date="2026-03-03"),
          Task("c","C",due_date="2026-03-04")]
    assert [row.task_id for row in due_between(rows,"2026-03-03","2026-03-03")]==["a","b"]


def test_due_between_can_include_completed_when_requested():
    rows=[Task("done","Done",completed=True,due_date="2026-03-03")]
    assert due_between(rows,"2026-03-03","2026-03-03")==[]
    assert len(due_between(rows,"2026-03-03","2026-03-03",include_done=True))==1


def test_due_soon_uses_explicit_reference_date():
    rows=[Task("a","A",due_date="2026-03-08"),Task("b","B",due_date="2026-03-09")]
    assert [task.task_id for task in due_soon(rows,"2026-03-01",days=7)]==["a"]


def test_overdue_excludes_today_and_completed_tasks():
    rows=[Task("old","Old",due_date="2026-03-01"),
          Task("today","Today",due_date="2026-03-02"),
          Task("done","Done",completed=True,due_date="2026-03-01")]
    assert [task.task_id for task in overdue_tasks(rows,"2026-03-02")] == ["old"]


def test_tag_completion_counts_each_tag_once_per_task():
    rows=[Task("a","A",completed=True,tags=("work","work")),Task("b","B",tags=("work",))]
    assert completion_by_tag(rows)=={"work":(1,2)}


def test_tag_count_can_skip_completed_rows():
    rows=[Task("a","A",completed=True,tags=("home",)),Task("b","B",tags=("work",))]
    assert tag_counts(rows,include_done=False)=={"work":1}


def test_daily_load_counts_only_tasks_with_dates():
    rows=[Task("a","A",due_date="2026-01-03"),Task("b","B",due_date="2026-01-03"),Task("c","C")]
    assert daily_load(rows)=={"2026-01-03":2}


def test_dashboard_has_deterministic_primitive_fields():
    row=Task("a","A",tags=("work",),due_date="2026-01-01")
    result=dashboard([row],"2026-01-02")
    assert result["total"]==1 and result["open"]==1
    assert result["overdue_ids"]==["a"] and result["tag_counts"]=={"work":1}


def test_due_window_rejects_reversed_range():
    with pytest.raises(ValueError): due_between([],"2026-03-02","2026-03-01")


def test_due_soon_rejects_negative_window():
    with pytest.raises(ValueError): due_soon([],"2026-03-01",days=-1)


def test_status_counts_preserve_both_buckets():
    assert status_counts([Task("a","A"),Task("b","B",completed=True)])=={"done":1,"open":1}


def test_tagged_ids_are_stable_and_can_skip_done():
    rows=[Task("b","B",tags=("work",)),Task("a","A",completed=True,tags=("work",))]
    assert tagged_task_ids(rows,"WORK")==("a","b")
    assert tagged_task_ids(rows,"work",include_done=False)==("b",)


def test_next_due_returns_earliest_open_item():
    rows=[Task("b","B",due_date="2026-02-02"),Task("a","A",due_date="2026-02-01")]
    assert next_due(rows,"2026-01-01").task_id=="a"


def test_compact_summary_is_plain_stable_text():
    assert compact_summary([Task("a","A")],"2026-01-01")=="1 open, 0 complete, 0 overdue"
