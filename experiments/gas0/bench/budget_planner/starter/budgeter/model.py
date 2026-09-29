"""Typed, JSON-friendly project records."""
from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from .amounts import parse_amount
from .dates import parse_date
from .errors import ValidationError

@dataclass
class Transaction:
    transaction_id: str
    day: str
    amount: Decimal
    category: str
    description: str = ""
    recurring: str | None = None

    def __post_init__(self):
        self.transaction_id = str(self.transaction_id).strip()
        if not self.transaction_id:
            raise ValidationError("transaction id is required")
        self.day = parse_date(self.day).isoformat()
        self.amount = parse_amount(self.amount)
        self.category = normalize_category(self.category)
        self.description = str(self.description).strip()

    def to_dict(self):
        from dataclasses import asdict
        row = asdict(self)
        row["amount"] = str(self.amount)
        return row

    @classmethod
    def from_dict(cls,row):
        return cls(**{key: row.get(key) for key in
                      ("transaction_id", "day", "amount", "category", "description", "recurring")})

@dataclass
class SavingsGoal:
    goal_id: str
    name: str
    target: Decimal
    saved: Decimal = Decimal("0.00")

    def __post_init__(self):
        self.goal_id = str(self.goal_id).strip()
        self.name = str(self.name).strip()
        self.target = parse_amount(self.target)
        self.saved = parse_amount(self.saved)
        if not self.goal_id or not self.name or self.target < 0 or self.saved < 0:
            raise ValidationError("invalid savings goal")

    @property
    def remaining(self):
        return max(Decimal("0.00"), self.target - self.saved)

    @property
    def complete(self):
        return self.saved >= self.target

def normalize_category(value):
    category=" ".join(str(value).split()).casefold()
    if not category: raise ValidationError("category is required")
    return category

def validate_transaction_ids(rows):
    ids=[row.transaction_id for row in rows]
    if len(ids)!=len(set(ids)): raise ValidationError("duplicate transaction id")
