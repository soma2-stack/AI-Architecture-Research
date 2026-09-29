from budgeter.model import Transaction
from budgeter.recurrence import expand_recurring

def test_recurrence_ids_are_stable_and_bounded():
    row=Transaction("r","2026-01-31","10","housing")
    a=expand_recurring(row,"2026-01","2026-03")
    b=expand_recurring(row,"2026-01","2026-03")
    assert [x.transaction_id for x in a]==[x.transaction_id for x in b]
    assert len(a)==3 and a[1].transaction_id=="r:2026-02"

def test_deferred_expansion_exists():
    assert callable(expand_recurring)
