from budgeter.model import Transaction
from budgeter.store import BudgetStore

def test_integer_cents_and_display_boundary():
    row=Transaction("a","2026-01-01","1.23","food")
    assert row.amount_cents==123 and str(row.amount)=="1.23"

def test_new_json_schema_stores_cents(tmp_path):
    s=BudgetStore(tmp_path/"b.json"); s.add(Transaction("a","2026-01-01","1.23","food")); s.save()
    text=s.path.read_text()
    assert '"amount_cents": 123' in text and '"amount"' not in text
