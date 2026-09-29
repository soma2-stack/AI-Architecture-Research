"""Date parsing helpers use calendar dates, never local wall-clock time."""
from datetime import date
from .errors import ValidationError


def parse_date(value):
    if value is None or value == "":
        return None
    try:
        parsed = date.fromisoformat(str(value))
    except ValueError as exc:
        raise ValidationError("date must use YYYY-MM-DD") from exc
    if parsed.isoformat() != str(value):
        raise ValidationError("date must use YYYY-MM-DD")
    return parsed.isoformat()


def is_overdue(due_date, today):
    due = parse_date(due_date)
    current = parse_date(today)
    return due is not None and current is not None and due < current


def date_sort_key(value):
    return value or "9999-12-31"


def earlier_date(left, right):
    left = parse_date(left)
    right = parse_date(right)
    if left is None:
        return right
    if right is None:
        return left
    return min(left, right)
