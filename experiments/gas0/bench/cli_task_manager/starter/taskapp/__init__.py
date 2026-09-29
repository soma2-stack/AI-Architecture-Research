"""Small offline task manager with deterministic JSON persistence."""
from .model import Task
from .store import TaskStore
from .commands import add_task, complete_task, update_title
from .query import list_tasks

__all__ = ["Task", "TaskStore", "add_task", "complete_task", "update_title", "list_tasks"]
