from budgeter.model import Transaction
from budgeter.query import after, before, category_month_matrix, select
from budgeter.validation import summarize_validation, validate_description


def records():
    return [Transaction("b", "2026-02-02", "-4", "Food"),
            Transaction("a", "2026-01-03", "8", "Travel"),
            Transaction("c", "2026-02-01", "2", "food")]


def test_select_composes_month_category_and_order():
    assert [r.transaction_id for r in select(records(), month="2026-02", category=" FOOD ")] == ["c", "b"]


def test_date_filters_are_strict():
    rows=records()
    assert [r.transaction_id for r in before(rows,"2026-02-01")] == ["a"]
    assert [r.transaction_id for r in after(rows,"2026-02-01")] == ["b"]


def test_month_matrix_is_sorted_and_counted():
    assert category_month_matrix(records())["food"] == {"2026-02": 2}


def test_validation_summary_has_stable_bounds():
    assert summarize_validation(records())["first_day"] == "2026-01-03"


def test_description_validation():
    assert validate_description("  lunch ") == "lunch"
