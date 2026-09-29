"""Stable task listing and filtering operations."""
from .dates import date_sort_key


def list_tasks(tasks, tag=None, include_done=True):
    rows = list(tasks)
    if tag is not None:
        wanted = str(tag).casefold()
        rows = [task for task in rows if wanted in task.tags]
    if not include_done:
        rows = [task for task in rows if not task.completed]
    return sorted(rows, key=lambda task: (task.completed, task.task_id))


def find_task(tasks, task_id):
    return next((task for task in tasks if task.task_id == task_id), None)


def search_title(tasks, query):
    needle = " ".join(str(query).split()).casefold()
    if not needle:
        return []
    return [task for task in tasks if needle in task.title.casefold()]


def count_open(tasks):
    return sum(not task.completed for task in tasks)


def count_by_tag(tasks):
    totals = {}
    for task in tasks:
        for tag in task.tags:
            totals[tag] = totals.get(tag, 0) + 1
    return dict(sorted(totals.items()))


def sort_by_due_date(tasks):
    return sorted(tasks, key=lambda task: (date_sort_key(task.due_date), task.task_id))


def completed_ids(tasks):
    return tuple(task.task_id for task in tasks if task.completed)
