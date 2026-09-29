"""Domain errors shown by both the library and the command line."""


class BudgetError(Exception):
    """Base class for expected input and storage failures."""


class ValidationError(BudgetError):
    """Raised when an amount, date, identifier, or category is invalid."""


class StorageError(BudgetError):
    """Raised when a saved budget cannot be read or written."""


def require(condition: bool, message: str) -> None:
    """Raise a stable user-facing validation error when condition is false."""
    if not condition:
        raise ValidationError(message)


def explain(error: Exception) -> str:
    """Return a concise deterministic message suitable for the CLI."""
    if isinstance(error, BudgetError):
        return str(error)
    return f"unexpected error: {type(error).__name__}"
