"""Category helpers use cent totals and stable group ordering."""
from collections import defaultdict
from decimal import Decimal
from .amounts import add_amounts
from .model import Transaction, normalize_category

DEFAULT_CATEGORIES=("food","housing","transport","health","other")
def known_categories(rows): return sorted(set(DEFAULT_CATEGORIES)|{row.category for row in rows})
def by_category(rows):
    groups=defaultdict(list)
    for row in rows: groups[normalize_category(row.category)].append(row)
    return dict(groups)
def totals(rows):
    return {name:add_amounts(row.amount for row in values)
            for name,values in sorted(by_category(rows).items())}
def category_count(rows): return len(known_categories(rows))
def filter_category(rows,category):
    if category is None: return list(rows)
    wanted=normalize_category(category)
    return [row for row in rows if row.category==wanted]
