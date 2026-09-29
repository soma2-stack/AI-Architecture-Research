"""Text presentation never controls persisted task state."""
from .dates import is_overdue
from .model import task_label


def format_task(task, today=None):
    text = task_label(task)
    if task.tags:
        text += " #" + " #".join(task.tags)
    if task.due_date:
        text += " due=" + task.due_date
        if today and not task.completed and is_overdue(task.due_date, today):
            text += " overdue"
    return text


def format_tasks(tasks, today=None):
    rows = [format_task(task, today) for task in tasks]
    return "\n".join(rows) if rows else "(no tasks)"


def format_summary(tasks):
    total = len(tasks)
    done = sum(task.completed for task in tasks)
    return f"{done}/{total} complete; {total - done} open"


def quote_field(value):
    text = str(value)
    return '"' + text.replace('"', '""') + '"' if any(ch in text for ch in ',"\n') else text


def table_row(task):
    return ",".join(quote_field(value) for value in
                    (task.task_id, task.title, task.due_date or "", "done" if task.completed else "open"))
