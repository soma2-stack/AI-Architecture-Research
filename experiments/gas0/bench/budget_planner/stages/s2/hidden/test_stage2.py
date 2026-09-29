from budgeter.budgets import CategoryBudgets
from budgeter.model import Transaction
from budgeter.summary import monthly_summary

def test_month_boundary_decision():
    rows=[Transaction("a","2026-03-31","-4","food"),
          Transaction("b","2026-04-01","-9","food")]
    b=CategoryBudgets(); b.set_limit("food","2026-03","20")
    assert monthly_summary(rows,"2026-03",b)["budget_status"]["food"]["actual"] == -4
    assert monthly_summary(rows,"2026-04",b)["budget_status"]["food"]["actual"] == -9

def test_budget_decimal_payload_contract():
    b=CategoryBudgets(); b.set_limit("food","2026-03","1.25")
    assert b.payload()["food|2026-03"] == "1.25"
