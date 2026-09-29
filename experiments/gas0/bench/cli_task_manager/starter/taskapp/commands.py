"""Mutations are small and return the changed record for callers."""
from dataclasses import replace
from .dates import parse_date
from .errors import MissingTask, ValidationError
from .ids import validate_id
from .model import Task, normalize_tags
from .query import find_task


def add_task(tasks, task_id, title, description="", tags=(), due_date=None):
    task_id = validate_id(task_id)
    if find_task(tasks, task_id) is not None:
        raise ValidationError("duplicate task id")
    task = Task(task_id, title, description, False, normalize_tags(tags), due_date)
    tasks.append(task)
    return task


def complete_task(tasks, task_id):
    task = find_task(tasks, task_id)
    if task is None:
        raise MissingTask(task_id)
    task.completed = True
    return task


def reopen_task(tasks, task_id):
    task = find_task(tasks, task_id)
    if task is None:
        raise MissingTask(task_id)
    task.completed = False
    return task


def update_title(tasks, task_id, title):
    task = find_task(tasks, task_id)
    if task is None:
        raise MissingTask(task_id)
    normalized = " ".join(str(title).split())
    if not normalized:
        raise ValidationError("title is required")
    task.title = normalized
    return task


def update_due_date(tasks, task_id, due_date):
    task = find_task(tasks, task_id)
    if task is None:
        raise MissingTask(task_id)
    task.due_date = parse_date(due_date)
    return task


def replace_tags(tasks, task_id, tags):
    task = find_task(tasks, task_id)
    if task is None:
        raise MissingTask(task_id)
    task.tags = normalize_tags(tags)
    return task


def remove_task(tasks, task_id):
    task = find_task(tasks, task_id)
    if task is None:
        raise MissingTask(task_id)
    tasks.remove(task)
    return task
