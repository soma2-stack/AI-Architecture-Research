"""Validated task records.

The starter schema deliberately stores completion as a Boolean. Later requests
change the persisted representation while preserving the public behavior.
"""
from __future__ import annotations
from dataclasses import dataclass
from .dates import parse_date
from .errors import ValidationError


@dataclass
class Task:
    task_id: str
    title: str
    description: str = ""
    completed: bool = False
    tags: tuple[str, ...] = ()
    due_date: str | None = None

    def __post_init__(self):
        self.task_id = str(self.task_id).strip()
        self.title = " ".join(str(self.title).split())
        self.description = str(self.description).strip()
        if not self.task_id or not self.title:
            raise ValidationError("task id and title are required")
        if not isinstance(self.completed, bool):
            raise ValidationError("completed must be Boolean")
        self.tags = normalize_tags(self.tags)
        if self.due_date is not None:
            self.due_date = parse_date(self.due_date)

    def to_dict(self):
        return {"task_id": self.task_id, "title": self.title,
                "description": self.description, "completed": self.completed,
                "tags": list(self.tags), "due_date": self.due_date}

    @classmethod
    def from_dict(cls, row):
        return cls(task_id=row["task_id"], title=row["title"],
                   description=row.get("description", ""),
                   completed=row.get("completed", False),
                   tags=tuple(row.get("tags", ())), due_date=row.get("due_date"))


def normalize_tags(values):
    """Normalize tags once so filters and saved output agree."""
    result = []
    for value in values or ():
        tag = " ".join(str(value).split()).casefold()
        if tag and tag not in result:
            result.append(tag)
    return tuple(sorted(result))


def task_identity(task):
    return task.task_id


def task_label(task):
    marker = "x" if task.completed else " "
    return f"[{marker}] {task.task_id}: {task.title}"
