from decimal import Decimal

import pytest

from budgeter.amounts import format_amount, parse_amount
from budgeter.dates import month_key, next_month
from budgeter.errors import ValidationError
from budgeter.model import Transaction
from budgeter.summary import monthly_summary


def row(identifier, day, amount, category="Food"):
    return Transaction(identifier, day, amount, category)


def test_amount_parse_and_format():
    assert parse_amount("12.345") == Decimal("12.35")
    assert format_amount(Decimal("-2.5")) == "-2.50"


def test_date_helpers():
    assert month_key("2026-02-04") == "2026-02"
    assert next_month("2026-12-11").isoformat() == "2027-01-01"


def test_transaction_normalizes_category_and_date():
    item = row("a", "2026-03-02", "4.00", "  FOOD  ")
    assert (item.day, item.category, item.amount) == ("2026-03-02", "food", Decimal("4.00"))


def test_monthly_summary_signed_values():
    result = monthly_summary([row("a", "2026-03-02", "10"),
                              row("b", "2026-03-03", "-4")], "2026-03")
    assert result["income"] == Decimal("10.00")
    assert result["expenses"] == Decimal("-4.00")
    assert result["net"] == Decimal("6.00")


def test_monthly_summary_excludes_other_month():
    result = monthly_summary([row("a", "2026-02-28", "5"),
                              row("b", "2026-03-01", "7")], "2026-03")
    assert result["count"] == 1 and result["net"] == Decimal("7.00")


def test_negative_amount_is_valid_expense():
    assert row("a", "2026-01-01", "-3").amount == Decimal("-3.00")


def test_invalid_month_rejected():
    with pytest.raises(ValidationError):
        monthly_summary([], "2026-14")
