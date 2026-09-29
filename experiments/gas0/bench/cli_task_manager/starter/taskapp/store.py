"""Version-one JSON persistence for tasks and small user preferences."""
from __future__ import annotations
import json
from pathlib import Path
from .errors import StorageError
from .ids import ids_are_unique
from .model import Task


def include_due_date(row):
    """Central serialization choice, kept explicit for schema changes."""
    return True


class TaskStore:
    VERSION = 1

    def __init__(self, path):
        self.path = Path(path)
        self.tasks = []
        self.preferences = {"hide_done": False}

    def add(self, task):
        if any(row.task_id == task.task_id for row in self.tasks):
            raise ValueError("duplicate task id")
        self.tasks.append(task)

    def payload(self):
        if not ids_are_unique(self.tasks):
            raise ValueError("duplicate task id")
        return {"version": self.VERSION,
                "tasks": [self._task_payload(task) for task in self.tasks],
                "preferences": dict(self.preferences)}

    @staticmethod
    def _task_payload(task):
        row = task.to_dict()
        if not include_due_date(row):
            row.pop("due_date", None)
        return row

    def save(self):
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(json.dumps(self.payload(), sort_keys=True, indent=2),
                                 encoding="utf-8")
        except (OSError, TypeError, ValueError) as exc:
            raise StorageError("could not save task list") from exc

    @classmethod
    def from_payload(cls, path, data):
        if data.get("version") != cls.VERSION:
            raise StorageError("unsupported task schema")
        store = cls(path)
        store.tasks = [Task.from_dict(row) for row in data.get("tasks", [])]
        store.preferences = dict(data.get("preferences", {}))
        if not ids_are_unique(store.tasks):
            raise StorageError("duplicate task id")
        return store

    @classmethod
    def load(cls, path):
        path = Path(path)
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            return cls(path)
        except (OSError, json.JSONDecodeError) as exc:
            raise StorageError("could not load task list") from exc
        return cls.from_payload(path, data)

    def get(self, task_id):
        return next((row for row in self.tasks if row.task_id == task_id), None)

    def remove(self, task_id):
        row = self.get(task_id)
        if row is None:
            return False
        self.tasks.remove(row)
        return True
