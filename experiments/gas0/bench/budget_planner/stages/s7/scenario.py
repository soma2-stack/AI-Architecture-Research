import json, tempfile
from pathlib import Path
from budgeter.store import BudgetStore
with tempfile.TemporaryDirectory() as folder:
    path=Path(folder)/"bad-but-valid.json"
    path.write_text(json.dumps({"version":2,"transactions":None}),encoding="utf-8")
    store=BudgetStore.load(path)
    assert store.transactions==[]
from budgeter.model import Transaction
from budgeter.recurrence import expand_recurring
row=Transaction("rent","2026-01-31","10","housing")
assert [item.day for item in expand_recurring(row,"2026-01","2026-02")] == ["2026-01-31","2026-02-28"]
