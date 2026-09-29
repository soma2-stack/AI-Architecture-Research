"""CSV adapters with explicit column ordering and stable error handling."""
from __future__ import annotations

import csv
import io

from .errors import ValidationError
from .model import Transaction


FIELDS = ("transaction_id", "day", "amount", "category", "description")


def export_csv(rows) -> str:
    """Serialize rows in deterministic date/id order."""
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    for row in sorted(rows, key=lambda item: (item.day, item.transaction_id)):
        writer.writerow({key: row.to_dict().get(key, "") for key in FIELDS})
    return stream.getvalue()


def import_csv(payload: str) -> list[Transaction]:
    """Parse a CSV document and reject missing required columns."""
    reader = csv.DictReader(io.StringIO(payload, newline=""))
    if reader.fieldnames is None or not set(FIELDS[:4]).issubset(reader.fieldnames):
        raise ValidationError("CSV is missing required columns")
    rows = []
    for line, row in enumerate(reader, 2):
        try:
            rows.append(Transaction.from_dict(row))
        except Exception as exc:
            raise ValidationError(f"invalid CSV row {line}") from exc
    ids = [row.transaction_id for row in rows]
    if len(ids) != len(set(ids)):
        raise ValidationError("duplicate transaction id in CSV")
    return rows


def merge_csv(existing, payload: str) -> list[Transaction]:
    """Merge imported rows by stable ID, replacing matching rows in place."""
    rows = list(existing)
    positions = {row.transaction_id: i for i, row in enumerate(rows)}
    for incoming in import_csv(payload):
        if incoming.transaction_id in positions:
            rows[positions[incoming.transaction_id]] = incoming
        else:
            positions[incoming.transaction_id] = len(rows)
            rows.append(incoming)
    return rows


def csv_row_count(payload: str) -> int:
    return max(0, sum(1 for _ in csv.DictReader(io.StringIO(payload))) )


def has_header(payload: str) -> bool:
    first = payload.splitlines()[0] if payload.splitlines() else ""
    return set(FIELDS[:4]).issubset(next(csv.reader([first]), []))
