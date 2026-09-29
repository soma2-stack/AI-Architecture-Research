from budgeter.model import Transaction
from budgeter.recurrence import expand_recurring

def test_month_end_is_clamped():
    row=Transaction("r","2026-01-31","10","housing")
    assert [x.day for x in expand_recurring(row,"2026-01","2026-03")] == ["2026-01-31","2026-02-28","2026-03-31"]
