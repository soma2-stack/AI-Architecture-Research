from budgeter.model import Transaction
from budgeter.recurrence import expand_recurring
from budgeter.store import BudgetStore

def test_recurring_round_trip_preserves_ids_and_cents(tmp_path):
    store=BudgetStore(tmp_path/"b.json")
    base=Transaction("rent","2026-01-31","10","housing")
    store.recurring=expand_recurring(base,"2026-01","2026-02")
    store.save(); loaded=BudgetStore.load(store.path)
    assert [r.transaction_id for r in loaded.recurring]==["rent:2026-01","rent:2026-02"]
    assert all(r.amount_cents==1000 for r in loaded.recurring)
