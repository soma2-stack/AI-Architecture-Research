"""Deterministic summaries for small personal task lists.

The module has no current-time dependency: callers pass the reference date so
that reports can be reproduced in tests, scripts, and saved project snapshots.
"""
from collections import Counter, defaultdict
from datetime import date, timedelta
from .dates import parse_date


def completion_ratio(tasks):
    rows = list(tasks)
    if not rows:
        return 0.0
    return sum(bool(task.completed) for task in rows) / len(rows)


def due_between(tasks, start, end, include_done=False):
    first = date.fromisoformat(parse_date(start))
    last = date.fromisoformat(parse_date(end))
    if last < first:
        raise ValueError("end must be on or after start")
    selected = []
    for task in tasks:
        if task.due_date is None or (task.completed and not include_done):
            continue
        day = date.fromisoformat(task.due_date)
        if first <= day <= last:
            selected.append(task)
    return sorted(selected, key=lambda task: (task.due_date, task.task_id))


def due_soon(tasks, today, days=7):
    current = date.fromisoformat(parse_date(today))
    if days < 0:
        raise ValueError("days cannot be negative")
    final = current + timedelta(days=days)
    return due_between(tasks, current.isoformat(), final.isoformat())


def overdue_tasks(tasks, today):
    current = date.fromisoformat(parse_date(today))
    return [task for task in due_between(tasks, "0001-01-01", current.isoformat())
            if task.due_date < current.isoformat()]


def tag_counts(tasks, include_done=True):
    counts = Counter()
    for task in tasks:
        if task.completed and not include_done:
            continue
        counts.update(task.tags)
    return dict(sorted(counts.items()))


def completion_by_tag(tasks):
    totals = defaultdict(lambda: [0, 0])
    for task in tasks:
        for tag in task.tags:
            totals[tag][0] += int(task.completed)
            totals[tag][1] += 1
    return {tag: (done, total) for tag, (done, total) in sorted(totals.items())}


def daily_load(tasks):
    counts = Counter(task.due_date for task in tasks if task.due_date is not None)
    return dict(sorted(counts.items()))


def dashboard(tasks, today):
    rows = list(tasks)
    return {"total": len(rows),
            "open": sum(not task.completed for task in rows),
            "complete": sum(task.completed for task in rows),
            "completion_ratio": completion_ratio(rows),
            "overdue_ids": [task.task_id for task in overdue_tasks(rows, today)],
            "tag_counts": tag_counts(rows),
            "daily_load": daily_load(rows)}


def status_counts(tasks):
    rows = list(tasks)
    return {"done": sum(task.completed for task in rows),
            "open": sum(not task.completed for task in rows)}


def tagged_task_ids(tasks, tag, include_done=True):
    wanted = str(tag).strip().casefold()
    return tuple(task.task_id for task in sorted(tasks, key=lambda row: row.task_id)
                 if wanted in task.tags and (include_done or not task.completed))


def next_due(tasks, today):
    rows = due_soon(tasks, today, days=3650)
    return rows[0] if rows else None


def compact_summary(tasks, today):
    report = dashboard(tasks, today)
    overdue = len(report["overdue_ids"])
    return (f"{report['open']} open, {report['complete']} complete, "
            f"{overdue} overdue")
