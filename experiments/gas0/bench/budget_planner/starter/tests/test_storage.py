import json

import pytest

from budgeter.csv_io import export_csv, import_csv
from budgeter.errors import StorageError, ValidationError
from budgeter.model import Transaction
from budgeter.store import BudgetStore


def test_add_find_replace_remove():
    store = BudgetStore("unused.json")
    first = Transaction("a", "2026-01-01", "1.00", "food")
    store.add(first)
    assert store.find("a") is first
    store.replace(Transaction("a", "2026-01-02", "2.00", "food"))
    assert store.find("a").amount == 2
    assert store.remove("a").day == "2026-01-02"


def test_json_round_trip(tmp_path):
    path = tmp_path / "budget.json"
    store = BudgetStore(path)
    store.add(Transaction("x", "2026-01-03", "-5.25", "Travel", "train"))
    store.save()
    loaded = BudgetStore.load(path)
    assert loaded.transactions[0].to_dict() == store.transactions[0].to_dict()


def test_csv_round_trip_and_stable_order():
    rows = [Transaction("b", "2026-01-02", "2", "food"),
            Transaction("a", "2026-01-01", "1", "other")]
    payload = export_csv(rows)
    loaded = import_csv(payload)
    assert [item.transaction_id for item in loaded] == ["a", "b"]


def test_csv_rejects_duplicate_ids():
    payload = "transaction_id,day,amount,category\na,2026-01-01,1,food\na,2026-01-02,2,food\n"
    with pytest.raises(ValidationError):
        import_csv(payload)


def test_corrupt_json_has_domain_error(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{", encoding="utf-8")
    with pytest.raises(StorageError):
        BudgetStore.load(path)


def test_payload_keeps_metadata():
    store = BudgetStore("unused.json")
    store.metadata["source"] = "test"
    assert json.loads(json.dumps(store.payload()))["metadata"]["source"] == "test"
