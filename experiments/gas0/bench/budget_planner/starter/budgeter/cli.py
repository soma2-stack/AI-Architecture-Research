"""Text-only command facade; never prompts interactively during tests."""
from __future__ import annotations

import argparse

from .amounts import format_amount
from .errors import BudgetError, explain
from .model import Transaction
from .store import BudgetStore
from .summary import monthly_summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="budgeter")
    parser.add_argument("--db", default="budget.json")
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add")
    add.add_argument("id"); add.add_argument("day"); add.add_argument("amount")
    add.add_argument("category"); add.add_argument("description", nargs="?", default="")
    listing = sub.add_parser("list")
    listing.add_argument("--category")
    summary = sub.add_parser("summary")
    summary.add_argument("month")
    return parser


def render_summary(row: dict) -> str:
    lines = [f"{row['month']} net {format_amount(row['net'])}"]
    for category, amount in row["categories"].items():
        lines.append(f"{category}: {format_amount(amount)}")
    return "\n".join(lines)


def dispatch(argv=None, store: BudgetStore | None = None) -> str:
    args = build_parser().parse_args(argv)
    store = store or BudgetStore(args.db)
    if args.command == "add":
        store.add(Transaction(args.id, args.day, args.amount, args.category, args.description))
        store.save()
        return f"added {args.id}"
    if args.command == "list":
        rows = store.sorted_transactions()
        if args.category:
            rows = [row for row in rows if row.category == args.category.casefold()]
        return "\n".join(f"{row.day} {row.transaction_id} {format_amount(row.amount)} {row.category}"
                         for row in rows)
    if args.command == "summary":
        return render_summary(monthly_summary(store.transactions, args.month))
    raise BudgetError("unknown command")


def main(argv=None) -> int:
    try:
        print(dispatch(argv))
        return 0
    except (BudgetError, ValueError, KeyError) as exc:
        print(explain(exc))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
