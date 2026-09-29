"""Deterministic summaries used by the CLI and later staged features."""
from decimal import Decimal
from .amounts import add_amounts
from .dates import month_key, validate_month
from .model import Transaction

def month_transactions(rows, month: str) -> list[Transaction]:
    validate_month(month)
    return [row for row in rows if month_key(row.day) == month]

def monthly_summary(rows, month: str) -> dict:
    """Return total, income, expenses, and category amounts."""
    selected = month_transactions(rows, month)
    income = add_amounts(row.amount for row in selected if row.amount > 0)
    expenses = add_amounts(row.amount for row in selected if row.amount < 0)
    categories = {}
    for row in selected:
        categories[row.category] = categories.get(row.category, Decimal("0.00")) + row.amount
    return {"month": month, "income": income, "expenses": expenses,
            "net": income + expenses, "categories": dict(sorted(categories.items())),
            "count": len(selected)}

def largest_expenses(rows, month: str, limit: int = 5):
    selected = [row for row in month_transactions(rows, month) if row.amount < 0]
    return sorted(selected, key=lambda row: (row.amount, row.day, row.transaction_id))[:max(0, limit)]

def average_expense(rows, month: str) -> Decimal:
    values = [abs(row.amount) for row in month_transactions(rows, month) if row.amount < 0]
    return add_amounts(values) / len(values) if values else Decimal("0.00")

def month_count(rows, month: str) -> int:
    return len(month_transactions(rows, month))
