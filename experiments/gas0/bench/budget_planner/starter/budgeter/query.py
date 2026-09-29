"""Composable transaction queries with deterministic result ordering."""
from __future__ import annotations

from .dates import month_key, parse_date
from .model import normalize_category


def select(rows, *, month=None, category=None, minimum=None, maximum=None):
    """Return a fresh list matching all supplied predicates."""
    selected = list(rows)
    if month is not None:
        selected = [row for row in selected if month_key(row.day) == month]
    if category is not None:
        wanted = normalize_category(category)
        selected = [row for row in selected if row.category == wanted]
    if minimum is not None:
        selected = [row for row in selected if row.amount >= minimum]
    if maximum is not None:
        selected = [row for row in selected if row.amount <= maximum]
    return sorted(selected, key=lambda row: (row.day, row.transaction_id))


def before(rows, day):
    """Select records strictly before a day."""
    boundary = parse_date(day)
    return [row for row in rows if parse_date(row.day) < boundary]


def after(rows, day):
    """Select records strictly after a day."""
    boundary = parse_date(day)
    return [row for row in rows if parse_date(row.day) > boundary]


def unique_categories(rows):
    return sorted({row.category for row in rows})


def total_count(rows, **filters):
    return len(select(rows, **filters))


def first_or_none(rows, **filters):
    selected = select(rows, **filters)
    return selected[0] if selected else None


def by_identifier(rows):
    return {row.transaction_id: row for row in rows}


def category_month_matrix(rows):
    """Build a sorted category/month count matrix for report summaries."""
    matrix = {}
    for row in rows:
        key = (row.category, month_key(row.day))
        matrix[key] = matrix.get(key, 0) + 1
    return {category: dict(sorted((month, count) for (name, month), count in matrix.items()
                                  if name == category))
            for category in sorted({name for name, _ in matrix})}


def validate_query_month(month):
    if len(month) != 7 or month[4] != "-":
        raise ValueError("month must use YYYY-MM")
    return month


def distinct_rows(rows):
    """Keep the first row for each ID without mutating input order."""
    seen = set()
    output = []
    for row in rows:
        if row.transaction_id not in seen:
            seen.add(row.transaction_id)
            output.append(row)
    return output


def group_by_month(rows):
    """Group rows into ordered YYYY-MM buckets."""
    groups = {}
    for row in sorted(rows, key=lambda item: (item.day, item.transaction_id)):
        groups.setdefault(month_key(row.day), []).append(row)
    return groups


def newest(rows, count=5):
    """Select the newest records with a stable identifier tie-break."""
    if count < 0:
        raise ValueError("count cannot be negative")
    return sorted(rows, key=lambda row: (row.day, row.transaction_id), reverse=True)[:count]


def sum_by_month(rows):
    """Return signed Decimal totals grouped by month."""
    from .amounts import add_amounts
    return {month: add_amounts(row.amount for row in group)
            for month, group in sorted(group_by_month(rows).items())}


def has_identifier(rows, identifier):
    return any(row.transaction_id == identifier for row in rows)


def without_identifier(rows, identifier):
    return [row for row in rows if row.transaction_id != identifier]
