"""Deterministic identifier utilities; no time or random dependency."""
from .errors import ValidationError


def validate_id(value):
    text = str(value).strip()
    if not text or any(ch.isspace() for ch in text):
        raise ValidationError("id must be nonempty and contain no spaces")
    if any(ch in "/\\" for ch in text):
        raise ValidationError("id cannot contain path separators")
    return text


def next_id(existing, prefix="t"):
    known = {str(value) for value in existing}
    index = 1
    while f"{prefix}{index}" in known:
        index += 1
    return f"{prefix}{index}"


def ids_are_unique(tasks):
    values = [task.task_id for task in tasks]
    return len(values) == len(set(values))


def stable_ids(tasks):
    return tuple(task.task_id for task in sorted(tasks, key=lambda item: item.task_id))
