from budgeter.store import BudgetStore

def test_recurring_expansion_is_still_deferred():
    assert not hasattr(BudgetStore, "expand_recurring")
