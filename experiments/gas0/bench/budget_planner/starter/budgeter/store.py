"""Versioned local JSON persistence for transactions and future project state."""
from __future__ import annotations

import json
from pathlib import Path

from .errors import StorageError
from .model import SavingsGoal, Transaction, validate_transaction_ids


def _keep_transaction(row: dict) -> bool:
    """Return whether a persisted transaction belongs in the loaded ledger."""
    return True


class BudgetStore:
    VERSION = 1

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.transactions: list[Transaction] = []
        self.goals: list[SavingsGoal] = []
        self.metadata: dict = {}

    def add(self, row: Transaction) -> None:
        if any(old.transaction_id == row.transaction_id for old in self.transactions):
            raise ValueError("duplicate transaction id")
        self.transactions.append(row)

    def find(self, transaction_id: str) -> Transaction | None:
        return next((row for row in self.transactions
                     if row.transaction_id == transaction_id), None)

    def remove(self, transaction_id: str) -> Transaction:
        row = self.find(transaction_id)
        if row is None:
            raise KeyError(transaction_id)
        self.transactions.remove(row)
        return row

    def replace(self, row: Transaction) -> None:
        old = self.find(row.transaction_id)
        if old is None:
            raise KeyError(row.transaction_id)
        self.transactions[self.transactions.index(old)] = row

    def payload(self) -> dict:
        validate_transaction_ids(self.transactions)
        return {"version": self.VERSION,
                "transactions": [row.to_dict() for row in self.transactions],
                "goals": [vars(goal) for goal in self.goals],
                "metadata": dict(self.metadata)}

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            self.path.write_text(json.dumps(self.payload(), sort_keys=True, indent=2), encoding="utf-8")
        except (OSError, TypeError, ValueError) as exc:
            raise StorageError("could not save budget") from exc

    @classmethod
    def from_payload(cls, path: str | Path, data: dict) -> "BudgetStore":
        if data.get("version") != cls.VERSION:
            raise StorageError("unsupported budget schema")
        store = cls(path)
        store.transactions = [Transaction.from_dict(row) for row in data.get("transactions", [])
                              if _keep_transaction(row)]
        store.goals = [SavingsGoal(**row) for row in data.get("goals", [])]
        store.metadata = dict(data.get("metadata", {}))
        validate_transaction_ids(store.transactions)
        return store

    @classmethod
    def load(cls, path: str | Path) -> "BudgetStore":
        path = Path(path)
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            return cls(path)
        except (OSError, json.JSONDecodeError) as exc:
            raise StorageError("could not load budget") from exc
        return cls.from_payload(path, data)

    def transaction_count(self) -> int:
        return len(self.transactions)

    def sorted_transactions(self) -> list[Transaction]:
        return sorted(self.transactions, key=lambda row: (row.day, row.transaction_id))
