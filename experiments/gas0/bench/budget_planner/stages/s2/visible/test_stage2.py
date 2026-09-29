from budgeter.budgets import CategoryBudgets
from budgeter.errors import ValidationError
from budgeter.model import Transaction
from budgeter.summary import monthly_summary

def test_limit_is_reported_with_actual():
    budgets=CategoryBudgets(); budgets.set_limit("food","2026-03","100")
    row=Transaction("x","2026-03-10","25","food")
    report=monthly_summary([row],"2026-03",budgets)
    assert report["budget_status"]["food"]["actual"] == 25
    assert report["budget_status"]["food"]["limit"] == 100

def test_negative_limit_rejected():
    import pytest
    with pytest.raises(ValidationError): CategoryBudgets().set_limit("food","2026-03",-1)
