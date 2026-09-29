"""Amount parsing and display helpers; starter storage uses decimal units."""
from __future__ import annotations

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from .errors import ValidationError


def parse_amount(value: str | int | float | Decimal) -> Decimal:
    """Parse a finite amount and quantize it to two decimal places."""
    try:
        amount = Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError) as exc:
        raise ValidationError("amount must be numeric") from exc
    if not amount.is_finite():
        raise ValidationError("amount must be finite")
    return amount


def format_amount(value: Decimal | int | float) -> str:
    """Render exactly two fractional digits without a currency symbol."""
    try:
        amount = Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError) as exc:
        raise ValidationError("amount must be numeric") from exc
    return f"{amount:.2f}"


def add_amounts(values) -> Decimal:
    """Sum values through Decimal conversion to avoid order-sensitive floats."""
    total = Decimal("0.00")
    for value in values:
        total += parse_amount(value)
    return total.quantize(Decimal("0.01"))


def nonnegative(value: Decimal) -> Decimal:
    """Validate values used for limits and targets."""
    if value < 0:
        raise ValidationError("amount cannot be negative")
    return value


def percentage(part: Decimal, whole: Decimal) -> Decimal:
    """Return a bounded percentage, with a zero target treated as complete."""
    if whole <= 0:
        return Decimal("100.00") if part >= 0 else Decimal("0.00")
    result = (part * Decimal("100") / whole).quantize(Decimal("0.01"))
    return min(Decimal("100.00"), max(Decimal("0.00"), result))
