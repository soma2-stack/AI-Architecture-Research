from budgeter.model import Transaction
from budgeter.store import BudgetStore

def test_recurring_rows_round_trip(tmp_path):
    store=BudgetStore(tmp_path/"b.json")
    store.recurring=[Transaction("r:2026-01","2026-01-31","5","food",recurring="monthly")]
    store.save(); loaded=BudgetStore.load(store.path)
    assert loaded.recurring[0].amount_cents==500
