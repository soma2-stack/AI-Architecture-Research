from budgeter.model import Transaction
from budgeter.store import BudgetStore

def test_zero_value_survives_round_trip(tmp_path):
    path=tmp_path/"budget.json"; store=BudgetStore(path)
    store.add(Transaction("zero","2026-01-01","0","other")); store.save()
    assert [row.transaction_id for row in BudgetStore.load(path).transactions] == ["zero"]
