from budgeter.store import BudgetStore

def test_zero_record_between_nonzero_records_keeps_order():
    data={"version":1,"transactions":[
      {"transaction_id":"a","day":"2026-01-01","amount":"1.00","category":"food"},
      {"transaction_id":"z","day":"2026-01-02","amount":"0.00","category":"food"},
      {"transaction_id":"b","day":"2026-01-03","amount":"-1.00","category":"food"}]}
    loaded=BudgetStore.from_payload("unused.json",data)
    assert [row.transaction_id for row in loaded.transactions] == ["a","z","b"]
