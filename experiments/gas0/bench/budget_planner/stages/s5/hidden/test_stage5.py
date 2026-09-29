from budgeter.model import Transaction
from budgeter.store import BudgetStore

def test_v1_migration_and_exact_cents():
    data={"version":1,"transactions":[
      {"transaction_id":"a","day":"2026-01-01","amount":"0.10","category":"food"},
      {"transaction_id":"b","day":"2026-01-01","amount":"0.20","category":"food"}]}
    s=BudgetStore.from_payload("unused",data)
    assert [r.amount_cents for r in s.transactions]==[10,20]
    s.add(Transaction("c","2026-01-01","0.30","food"))
    assert sum(r.amount_cents for r in s.transactions)==60
