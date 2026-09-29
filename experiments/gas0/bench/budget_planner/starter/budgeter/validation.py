"""Cross-record validation kept outside the storage implementation."""
from __future__ import annotations

from collections import Counter

from .dates import parse_date
from .errors import ValidationError
from .model import normalize_category


def validate_description(text, maximum=240):
    value = str(text)
    if len(value) > maximum:
        raise ValidationError("description is too long")
    if "\x00" in value:
        raise ValidationError("description contains a null character")
    return value.strip()


def validate_rows(rows):
    """Check identifiers, dates, categories, and normalized amount values."""
    identifiers = [row.transaction_id for row in rows]
    duplicates = sorted(name for name, count in Counter(identifiers).items() if count > 1)
    if duplicates:
        raise ValidationError("duplicate transaction id")
    for row in rows:
        parse_date(row.day)
        normalize_category(row.category)
        validate_description(row.description)
        if not row.amount.is_finite():
            raise ValidationError("amount must be finite")
    return True


def summarize_validation(rows):
    """Return a deterministic count-only audit record."""
    validate_rows(rows)
    return {"rows": len(rows), "categories": len({row.category for row in rows}),
            "first_day": min((row.day for row in rows), default=None),
            "last_day": max((row.day for row in rows), default=None)}


def validate_goal_names(goals):
    names = [goal.name.casefold() for goal in goals]
    if len(names) != len(set(names)):
        raise ValidationError("duplicate savings goal name")
    return True


def validate_budget_keys(budgets):
    for category, month in budgets:
        normalize_category(category)
        if len(month) != 7:
            raise ValidationError("invalid budget month")
    return True


def record_summary(rows):
    """Expose only stable, non-sensitive aggregate fields."""
    result = summarize_validation(rows)
    result["categories"] = sorted({row.category for row in rows})
    return result


def duplicate_identifier_report(rows):
    """Expose duplicate IDs for preview tools without changing or rejecting rows."""
    counts = Counter(row.transaction_id for row in rows)
    return {identifier: count for identifier, count in sorted(counts.items()) if count > 1}


def dates_in_order(rows):
    """Check the canonical display order used by reports and exports."""
    keys = [(parse_date(row.day), row.transaction_id) for row in rows]
    return keys == sorted(keys)


def missing_descriptions(rows):
    """Return IDs that lack human-readable descriptions, in stable order."""
    return sorted(row.transaction_id for row in rows if not row.description.strip())


def category_spellings(rows):
    """Return raw spellings grouped by their normalized category."""
    result = {}
    for row in rows:
        result.setdefault(normalize_category(row.category), set()).add(row.category)
    return {key: sorted(values) for key, values in sorted(result.items())}


def summary_is_finite(summary):
    """Guard report consumers from non-finite numeric values."""
    for value in summary.values():
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            if value != value or value in {float("inf"), float("-inf")}:
                return False
    return True
