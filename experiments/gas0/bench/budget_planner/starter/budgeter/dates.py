"""Strict date helpers used by CSV import and period summaries."""
from __future__ import annotations

from datetime import date, datetime

from .errors import ValidationError


def parse_date(value: str | date) -> date:
    """Parse ISO dates; datetime values are normalized to their date."""
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError("date must use YYYY-MM-DD") from exc


def month_start(value: str | date) -> date:
    """Return the first date in the month containing value."""
    parsed = parse_date(value)
    return date(parsed.year, parsed.month, 1)


def next_month(value: str | date) -> date:
    """Return the first date of the following month."""
    current = month_start(value)
    return date(current.year + (current.month == 12), current.month % 12 + 1, 1)


def month_key(value: str | date) -> str:
    """Format a date as the stable YYYY-MM report key."""
    parsed = parse_date(value)
    return f"{parsed.year:04d}-{parsed.month:02d}"


def in_month(value: str | date, month: str) -> bool:
    """Starter period membership helper; Stage 2 defines boundary semantics."""
    parsed = parse_date(value)
    return month_key(parsed) == month


def validate_month(month: str) -> tuple[int, int]:
    """Validate YYYY-MM and return its integer components."""
    try:
        year_text, month_text = month.split("-", 1)
        year, number = int(year_text), int(month_text)
        if len(year_text) != 4 or not 1 <= number <= 12:
            raise ValueError
        return year, number
    except (ValueError, AttributeError) as exc:
        raise ValidationError("month must use YYYY-MM") from exc
