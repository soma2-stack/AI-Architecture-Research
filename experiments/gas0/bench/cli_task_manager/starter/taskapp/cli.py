"""Simple command dispatcher suitable for tests and terminal use."""
from __future__ import annotations
import argparse
from .commands import add_task, complete_task, reopen_task, update_title
from .errors import TaskError
from .formatting import format_summary, format_tasks
from .query import list_tasks
from .store import TaskStore


def dispatch(store, argv):
    parser = argparse.ArgumentParser(prog="tasks")
    commands = parser.add_subparsers(dest="command", required=True)
    create = commands.add_parser("add")
    create.add_argument("id"); create.add_argument("title")
    commands.add_parser("list")
    done = commands.add_parser("done"); done.add_argument("id")
    reopen = commands.add_parser("reopen"); reopen.add_argument("id")
    rename = commands.add_parser("rename"); rename.add_argument("id"); rename.add_argument("title")
    commands.add_parser("summary")
    args = parser.parse_args(argv)
    try:
        if args.command == "add":
            task = add_task(store.tasks, args.id, args.title)
            store.save(); return task.task_id
        if args.command == "done":
            complete_task(store.tasks, args.id); store.save(); return "done"
        if args.command == "reopen":
            reopen_task(store.tasks, args.id); store.save(); return "open"
        if args.command == "rename":
            update_title(store.tasks, args.id, args.title); store.save(); return "updated"
        if args.command == "list":
            return format_tasks(list_tasks(store.tasks))
        return format_summary(store.tasks)
    except TaskError as exc:
        return f"error: {exc}"


def main(argv=None, path="tasks.json"):
    store = TaskStore.load(path)
    result = dispatch(store, argv)
    print(result)
    return 0 if not str(result).startswith("error:") else 2
