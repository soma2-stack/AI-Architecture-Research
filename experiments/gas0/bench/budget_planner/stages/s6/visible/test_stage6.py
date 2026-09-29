from budgeter.model import Transaction

def test_amount_state_is_an_integer():
    row=Transaction("a","2026-01-01","2.34","food")
    assert isinstance(row.amount_cents,int) and row.amount_cents==234
