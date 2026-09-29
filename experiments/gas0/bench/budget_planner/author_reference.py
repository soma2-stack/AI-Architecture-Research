"""Build the calibration project's staged requests, tests and reference patches."""
from __future__ import annotations

import difflib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STARTER = ROOT / "starter"
STAGES = ROOT / "stages"
REFERENCE = ROOT / "reference"


def snapshot():
    return {p.relative_to(STARTER).as_posix(): p.read_text(encoding="utf-8")
            for p in STARTER.rglob("*.py")}


def patch_text(before, after):
    out = []
    for name in sorted(set(before) | set(after)):
        old = before.get(name, "").splitlines(keepends=True)
        new = after.get(name, "").splitlines(keepends=True)
        if old != new:
            out.extend(difflib.unified_diff(old, new,
                fromfile=f"a/{name}" if name in before else "/dev/null",
                tofile=f"b/{name}" if name in after else "/dev/null"))
    return "".join(out)


def write_patch(stage, before, after):
    (REFERENCE / f"s{stage}.patch").write_bytes(patch_text(before, after).encode("utf-8"))


def put(stage, folder, name, body):
    path = STAGES / f"s{stage}" / folder / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body.strip() + "\n", encoding="utf-8")


def replace(files, name, old, new):
    if files[name].count(old) != 1:
        raise AssertionError((name, old, files[name].count(old)))
    files[name] = files[name].replace(old, new)


def add(files, name, body):
    if name in files:
        raise AssertionError(f"duplicate file {name}")
    files[name] = body.strip() + "\n"


def save_state(files):
    for path in STARTER.rglob("*.py"):
        path.unlink()
    for name, body in files.items():
        path = STARTER / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")


def main():
    for path in (STAGES, REFERENCE):
        if path.exists():
            shutil.rmtree(path)
    REFERENCE.mkdir(parents=True)
    files = snapshot()
    state = files.copy()
    (REFERENCE / "s1.patch").write_bytes(b"")

    put(1, "", "request.md", """Do not edit. Inspect the project and return JSON with exactly q1 through q8: q1 the amount parser; q2 the transaction fields; q3 the date format; q4 the monthly summary entry point; q5 category normalization; q6 saved schema version; q7 CSV import entry point; q8 CLI command that prints a monthly summary. Use exact names and values.""")

    # Stage 2: monthly category budgets.
    add(state, "budgeter/budgets.py", '''from decimal import Decimal
from .amounts import nonnegative, parse_amount
from .dates import validate_month
from .model import normalize_category

class CategoryBudgets:
    def __init__(self, limits=None):
        self.limits = {key: parse_amount(value) for key, value in (limits or {}).items()}

    def set_limit(self, category, month, amount):
        validate_month(month)
        value = nonnegative(parse_amount(amount))
        self.limits[(normalize_category(category), month)] = value
        return value

    def get_limit(self, category, month):
        validate_month(month)
        return self.limits.get((normalize_category(category), month), Decimal("0.00"))

    def payload(self):
        return {f"{category}|{month}": str(value)
                for (category, month), value in sorted(self.limits.items())}

    @classmethod
    def from_payload(cls, payload):
        values = {}
        for key, value in payload.items():
            category, month = key.split("|", 1)
            values[(category, month)] = value
        return cls(values)

    def categories(self, month):
        validate_month(month)
        return sorted(category for category, key_month in self.limits if key_month == month)
''')
    replace(state, "budgeter/store.py", '        self.goals: list[SavingsGoal] = []\n', '        self.goals: list[SavingsGoal] = []\n        self.budgets: dict = {}\n')
    replace(state, "budgeter/store.py", '                "metadata": dict(self.metadata)}\n', '                "budgets": dict(self.budgets),\n                "metadata": dict(self.metadata)}\n')
    replace(state, "budgeter/store.py", '        store.metadata = dict(data.get("metadata", {}))\n', '        store.metadata = dict(data.get("metadata", {}))\n        store.budgets = dict(data.get("budgets", {}))\n')
    replace(state, "budgeter/summary.py", "def monthly_summary(rows, month: str) -> dict:\n", "def monthly_summary(rows, month: str, budgets=None) -> dict:\n")
    replace(state, "budgeter/summary.py", '''    return {"month": month, "income": income, "expenses": expenses,
            "net": income + expenses, "categories": dict(sorted(categories.items())),
            "count": len(selected)}
''', '''    limits = budgets or {}
    if hasattr(limits, "payload"):
        limits = limits.payload()
    status = {name: {"actual": amount,
                     "limit": Decimal(limits.get(f"{name}|{month}", "0.00"))}
              for name, amount in sorted(categories.items())}
    return {"month": month, "income": income, "expenses": expenses,
            "net": income + expenses, "categories": dict(sorted(categories.items())),
            "budget_status": status, "count": len(selected)}
''')
    replace(state, "budgeter/__init__.py", "from .summary import monthly_summary\n", "from .summary import monthly_summary\nfrom .budgets import CategoryBudgets\n")
    replace(state, "budgeter/__init__.py", '"BudgetStore", "monthly_summary"]', '"BudgetStore", "monthly_summary", "CategoryBudgets"]')
    put(2, "", "request.md", """Add per-category monthly budget limits and report actual spending against each limit for a requested month. Designer decision D2.1: month intervals include their first day and exclude the first day of the next month. Keep existing behavior unless explicitly changed.""")
    put(2, "visible", "test_stage2.py", '''from budgeter.budgets import CategoryBudgets
from budgeter.errors import ValidationError
from budgeter.model import Transaction
from budgeter.summary import monthly_summary

def test_limit_is_reported_with_actual():
    budgets=CategoryBudgets(); budgets.set_limit("food","2026-03","100")
    row=Transaction("x","2026-03-10","25","food")
    report=monthly_summary([row],"2026-03",budgets)
    assert report["budget_status"]["food"]["actual"] == 25
    assert report["budget_status"]["food"]["limit"] == 100

def test_negative_limit_rejected():
    import pytest
    with pytest.raises(ValidationError): CategoryBudgets().set_limit("food","2026-03",-1)
''')
    put(2, "hidden", "test_stage2.py", '''from budgeter.budgets import CategoryBudgets
from budgeter.model import Transaction
from budgeter.summary import monthly_summary

def test_month_boundary_decision():
    rows=[Transaction("a","2026-03-31","-4","food"),
          Transaction("b","2026-04-01","-9","food")]
    b=CategoryBudgets(); b.set_limit("food","2026-03","20")
    assert monthly_summary(rows,"2026-03",b)["budget_status"]["food"]["actual"] == -4
    assert monthly_summary(rows,"2026-04",b)["budget_status"]["food"]["actual"] == -9

def test_budget_decimal_payload_contract():
    b=CategoryBudgets(); b.set_limit("food","2026-03","1.25")
    assert b.payload()["food|2026-03"] == "1.25"
''')
    put(2, "", "supersedes.json", "[]")
    put(2, "", "unused.txt", "stage package metadata placeholder")
    write_patch(2, files, state)
    files = state.copy()

    # Stage 3: goals, refund decision and deferred recurring expansion.
    add(state, "budgeter/goals.py", '''from .amounts import nonnegative, parse_amount, percentage
from .errors import ValidationError
from .model import SavingsGoal

def add_goal(goals, goal_id, name, target):
    if any(goal.goal_id == goal_id for goal in goals):
        raise ValidationError("duplicate goal id")
    goal = SavingsGoal(goal_id, name, nonnegative(parse_amount(target)))
    goals.append(goal)
    return goal

def contribute(goal, amount):
    value = nonnegative(parse_amount(amount))
    goal.saved += value
    return goal.remaining

def goal_report(goals):
    return [{"id": g.goal_id, "name": g.name, "target": g.target,
             "saved": g.saved, "remaining": g.remaining,
             "complete": g.complete, "percent": percentage(g.saved, g.target)}
            for g in sorted(goals, key=lambda item: item.goal_id)]

def find_goal(goals, goal_id):
    return next((goal for goal in goals if goal.goal_id == goal_id), None)

def remove_goal(goals, goal_id):
    goal=find_goal(goals,goal_id)
    if goal is None: raise KeyError(goal_id)
    goals.remove(goal)
    return goal
''')
    replace(state, "budgeter/__init__.py", "from .budgets import CategoryBudgets\n", "from .budgets import CategoryBudgets\nfrom .goals import add_goal, contribute, goal_report\n")
    replace(state, "budgeter/__init__.py", '"CategoryBudgets"]', '"CategoryBudgets", "add_goal", "contribute", "goal_report"]')
    replace(state, "budgeter/store.py", '"goals": [vars(goal) for goal in self.goals],', '"goals": [{"goal_id":g.goal_id,"name":g.name,"target":str(g.target),"saved":str(g.saved)} for g in self.goals],')
    put(3, "", "request.md", """Add named savings goals with a target, contributions, and progress reporting. Designer decision D3.1: refunds are negative expenses and reduce actual category spending. Defer recurring-transaction expansion; do not implement it yet because it is required later.""")
    put(3, "visible", "test_stage3.py", '''from budgeter.goals import add_goal, contribute, goal_report
from budgeter.errors import ValidationError

def test_goal_progress_and_completion():
    goals=[]; goal=add_goal(goals,"g1","Trip","100")
    assert contribute(goal,"35") == 65
    assert goal_report(goals)[0]["complete"] is False
    contribute(goal,"65")
    assert goal_report(goals)[0]["complete"] is True

def test_duplicate_goal_rejected():
    import pytest
    goals=[]; add_goal(goals,"g1","Trip","10")
    with pytest.raises(ValidationError): add_goal(goals,"g1","Other","20")
''')
    put(3, "hidden", "test_stage3.py", '''from budgeter.goals import add_goal, contribute
from budgeter.model import Transaction
from budgeter.summary import monthly_summary

def test_refund_reduces_actual_category_spend():
    rows=[Transaction("a","2026-04-04","-40","travel"),
          Transaction("b","2026-04-08","15","travel")]
    report=monthly_summary(rows,"2026-04")
    assert report["categories"]["travel"] == -25
    assert report["expenses"] == -40 and report["income"] == 15

def test_goal_contribution_does_not_change_transaction_report():
    rows=[Transaction("a","2026-04-04","-4","food")]
    goal=add_goal([],"g","Reserve","12"); contribute(goal,"5")
    assert monthly_summary(rows,"2026-04")["net"] == -4
''')
    put(3, "hidden", "test_stage3_deferred.py", '''from budgeter.store import BudgetStore

def test_recurring_expansion_is_still_deferred():
    assert not hasattr(BudgetStore, "expand_recurring")
''')
    put(3, "", "supersedes.json", "[]")
    write_patch(3, files, state)
    files = state.copy()

    # Stage 4 injection is a regression only in the new zero-row behavior.
    old = 'def _keep_transaction(row: dict) -> bool:\n    """Return whether a persisted transaction belongs in the loaded ledger."""\n    return True\n'
    injected = 'def _keep_transaction(row: dict) -> bool:\n    """Return whether a persisted transaction belongs in the loaded ledger."""\n    return str(row.get("amount", "")).strip() not in {"0", "0.00", "0.0"}\n'
    bugged = state.copy()
    replace(bugged, "budgeter/store.py", old, injected)
    (STAGES / "s4").mkdir(parents=True, exist_ok=True)
    (STAGES / "s4" / "bug.patch").write_bytes(
        patch_text(state, bugged).replace("\r\n", "\n").encode("utf-8"))
    state = bugged
    put(4, "", "request.md", """After loading a saved budget, a zero-value transaction is missing from the list. Diagnose and fix the issue without changing the saved schema.""")
    put(4, "visible", "test_stage4.py", '''from budgeter.model import Transaction
from budgeter.store import BudgetStore

def test_zero_value_survives_round_trip(tmp_path):
    path=tmp_path/"budget.json"; store=BudgetStore(path)
    store.add(Transaction("zero","2026-01-01","0","other")); store.save()
    assert [row.transaction_id for row in BudgetStore.load(path).transactions] == ["zero"]
''')
    put(4, "hidden", "test_stage4.py", '''from budgeter.store import BudgetStore

def test_zero_record_between_nonzero_records_keeps_order():
    data={"version":1,"transactions":[
      {"transaction_id":"a","day":"2026-01-01","amount":"1.00","category":"food"},
      {"transaction_id":"z","day":"2026-01-02","amount":"0.00","category":"food"},
      {"transaction_id":"b","day":"2026-01-03","amount":"-1.00","category":"food"}]}
    loaded=BudgetStore.from_payload("unused.json",data)
    assert [row.transaction_id for row in loaded.transactions] == ["a","z","b"]
''')
    put(4, "", "supersedes.json", "[]")
    fixed = state.copy()
    replace(fixed, "budgeter/store.py", injected, old)
    write_patch(4, state, fixed)
    state = fixed
    files = state.copy()

    # Stage 5: make integer cents the internal and persisted monetary representation.
    state["budgeter/model.py"] = '''"""Typed, JSON-friendly project records."""
from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from .amounts import parse_amount
from .dates import parse_date
from .errors import ValidationError

@dataclass(init=False)
class Transaction:
    transaction_id: str
    day: str
    amount_cents: int
    category: str
    description: str
    recurring: str | None

    def __init__(self, transaction_id, day, amount, category, description="", recurring=None):
        self.transaction_id=str(transaction_id).strip()
        if not self.transaction_id: raise ValidationError("transaction id is required")
        self.day=parse_date(day).isoformat()
        self.amount_cents=int(parse_amount(amount)*100)
        self.category=normalize_category(category)
        self.description=str(description).strip()
        self.recurring=recurring

    @property
    def amount(self):
        """Decimal display boundary; calculations use amount_cents."""
        return Decimal(self.amount_cents)/100

    @property
    def amount_value(self):
        return self.amount

    def to_dict(self):
        return {"transaction_id":self.transaction_id,"day":self.day,
                "amount_cents":self.amount_cents,"category":self.category,
                "description":self.description,"recurring":self.recurring}

    @classmethod
    def from_dict(cls,row):
        cents=row.get("amount_cents")
        amount=Decimal(int(cents))/100 if cents is not None else row.get("amount",0)
        return cls(row.get("transaction_id"),row.get("day"),amount,
                   row.get("category"),row.get("description", ""),row.get("recurring"))

@dataclass(init=False)
class SavingsGoal:
    goal_id: str
    name: str
    target_cents: int
    saved_cents: int

    def __init__(self,goal_id,name,target,saved=0):
        self.goal_id=str(goal_id).strip(); self.name=str(name).strip()
        self.target_cents=int(parse_amount(target)*100)
        self.saved_cents=int(parse_amount(saved)*100)
        if not self.goal_id or not self.name or self.target_cents<0 or self.saved_cents<0:
            raise ValidationError("invalid savings goal")

    @property
    def target(self): return Decimal(self.target_cents)/100
    @property
    def saved(self): return Decimal(self.saved_cents)/100
    @property
    def remaining(self): return Decimal(max(0,self.target_cents-self.saved_cents))/100
    @property
    def complete(self): return self.saved_cents>=self.target_cents
    def to_dict(self):
        return {"goal_id":self.goal_id,"name":self.name,
                "target_cents":self.target_cents,"saved_cents":self.saved_cents}
    @classmethod
    def from_dict(cls,row):
        obj=cls(row["goal_id"],row["name"],0,0)
        obj.target_cents=int(row.get("target_cents",int(parse_amount(row.get("target",0))*100)))
        obj.saved_cents=int(row.get("saved_cents",int(parse_amount(row.get("saved",0))*100)))
        return obj

def normalize_category(value):
    category=" ".join(str(value).split()).casefold()
    if not category: raise ValidationError("category is required")
    return category

def validate_transaction_ids(rows):
    ids=[row.transaction_id for row in rows]
    if len(ids)!=len(set(ids)): raise ValidationError("duplicate transaction id")
'''
    state["budgeter/budgets.py"] = '''from .amounts import parse_amount
from .dates import validate_month
from .errors import ValidationError
from .model import normalize_category

class CategoryBudgets:
    """Budget limits are stored and compared as integer cents."""
    def __init__(self,limits=None):
        self.limits={}
        for key,value in (limits or {}).items():
            self.limits[key]=int(parse_amount(value)*100)
    def set_limit(self,category,month,amount):
        validate_month(month); cents=int(parse_amount(amount)*100)
        if cents<0: raise ValidationError("amount cannot be negative")
        self.limits[(normalize_category(category),month)]=cents
        return cents
    def get_limit(self,category,month):
        validate_month(month)
        return self.limits.get((normalize_category(category),month),0)
    def payload(self):
        return {f"{category}|{month}":cents for (category,month),cents in sorted(self.limits.items())}
    @classmethod
    def from_payload(cls,payload):
        obj=cls(); obj.limits={tuple(key.split("|",1)):int(value) for key,value in payload.items()}
        return obj
    def categories(self,month):
        validate_month(month)
        return sorted(category for category,key_month in self.limits if key_month==month)
'''
    state["budgeter/goals.py"] = '''from .amounts import parse_amount, percentage
from .errors import ValidationError
from .model import SavingsGoal

def add_goal(goals,goal_id,name,target):
    if any(goal.goal_id==goal_id for goal in goals): raise ValidationError("duplicate goal id")
    goal=SavingsGoal(goal_id,name,target); goals.append(goal); return goal
def contribute(goal,amount):
    cents=int(parse_amount(amount)*100)
    if cents<0: raise ValueError("contribution cannot be negative")
    goal.saved_cents+=cents
    return goal.remaining
def goal_report(goals):
    return [{"id":g.goal_id,"name":g.name,"target":g.target,"saved":g.saved,
             "remaining":g.remaining,"complete":g.complete,
             "percent":percentage(g.saved,g.target)}
            for g in sorted(goals,key=lambda item:item.goal_id)]
def find_goal(goals,goal_id):
    return next((goal for goal in goals if goal.goal_id==goal_id),None)
def remove_goal(goals,goal_id):
    goal=find_goal(goals,goal_id)
    if goal is None: raise KeyError(goal_id)
    goals.remove(goal); return goal
'''
    state["budgeter/summary.py"] = '''"""Deterministic reports; arithmetic is performed in integer cents."""
from decimal import Decimal
from .dates import month_key, validate_month
from .model import Transaction

def month_transactions(rows,month):
    validate_month(month)
    return [row for row in rows if month_key(row.day)==month]
def monthly_summary(rows,month,budgets=None,goals=None):
    selected=month_transactions(rows,month)
    income_cents=sum(row.amount_cents for row in selected if row.amount_cents>0)
    expense_cents=sum(row.amount_cents for row in selected if row.amount_cents<0)
    totals={}
    for row in selected: totals[row.category]=totals.get(row.category,0)+row.amount_cents
    categories={key:Decimal(value)/100 for key,value in sorted(totals.items())}
    limits=budgets or {}
    if hasattr(limits,"payload"): limits=limits.payload()
    budget_status={name:{"actual":amount,"limit":Decimal(limits.get(f"{name}|{month}",0))/100}
                   for name,amount in categories.items()}
    return {"month":month,"income":Decimal(income_cents)/100,
            "expenses":Decimal(expense_cents)/100,
            "net":Decimal(income_cents+expense_cents)/100,
            "categories":categories,"budget_status":budget_status,
            "goals":goals or [],"count":len(selected)}
def largest_expenses(rows,month,limit=5):
    selected=[row for row in month_transactions(rows,month) if row.amount_cents<0]
    return sorted(selected,key=lambda row:(row.amount_cents,row.day,row.transaction_id))[:max(0,limit)]
def average_expense(rows,month):
    values=[-row.amount_cents for row in month_transactions(rows,month) if row.amount_cents<0]
    return Decimal(sum(values),).scaleb(-2)/len(values) if values else Decimal("0.00")
def month_count(rows,month): return len(month_transactions(rows,month))
'''
    # Decimal construction from an integer is exact; remove any accidental tuple-like syntax.
    replace(state,"budgeter/summary.py","Decimal(sum(values),).scaleb(-2)","Decimal(sum(values)).scaleb(-2)")
    state["budgeter/categories.py"] = '''"""Category helpers use cent totals and stable group ordering."""
from collections import defaultdict
from decimal import Decimal
from .model import Transaction, normalize_category

DEFAULT_CATEGORIES=("food","housing","transport","health","other")
def known_categories(rows): return sorted(set(DEFAULT_CATEGORIES)|{row.category for row in rows})
def by_category(rows):
    groups=defaultdict(list)
    for row in rows: groups[normalize_category(row.category)].append(row)
    return dict(groups)
def totals(rows):
    return {name:Decimal(sum(row.amount_cents for row in values)).scaleb(-2)
            for name,values in sorted(by_category(rows).items())}
def category_count(rows): return len(known_categories(rows))
def filter_category(rows,category):
    if category is None: return list(rows)
    wanted=normalize_category(category)
    return [row for row in rows if row.category==wanted]
'''
    # Save the complete integer-cent implementation for Stage 6. Stage 5 only
    # changes transaction storage/persistence; budgets and goals remain Decimal
    # until the persistent global invariant is introduced in Stage 6.
    stage6_modules = {name: state[name] for name in (
        "budgeter/model.py", "budgeter/budgets.py", "budgeter/goals.py",
        "budgeter/summary.py", "budgeter/categories.py")}
    model = state["budgeter/model.py"]
    goal_marker = "@dataclass(init=False)\nclass SavingsGoal:"
    tail_marker = "\ndef normalize_category"
    model_prefix, model_tail = model.split(goal_marker, 1)
    _, model_suffix = model_tail.split(tail_marker, 1)
    baseline_model = files["budgeter/model.py"]
    baseline_goal_marker = "@dataclass\nclass SavingsGoal:"
    _, baseline_tail = baseline_model.split(baseline_goal_marker, 1)
    baseline_goal, _ = baseline_tail.split(tail_marker, 1)
    state["budgeter/model.py"] = (
        model_prefix + baseline_goal_marker + baseline_goal +
        tail_marker + model_suffix)
    for name in ("budgeter/budgets.py", "budgeter/goals.py",
                 "budgeter/summary.py", "budgeter/categories.py"):
        state[name] = files[name]
    replace(state,"budgeter/store.py","    VERSION = 1","    VERSION = 2")
    replace(state,"budgeter/store.py",'if data.get("version") != cls.VERSION:', 'if data.get("version") not in {1, cls.VERSION}:')
    replace(state,"budgeter/csv_io.py",'FIELDS = ("transaction_id", "day", "amount", "category", "description")', 'FIELDS = ("transaction_id", "day", "amount", "category", "description")')
    replace(state,"budgeter/csv_io.py",'import csv\n', 'import csv\nfrom .amounts import format_amount\n')
    replace(state,"budgeter/csv_io.py",'writer.writerow({key: row.to_dict().get(key, "") for key in FIELDS})', 'writer.writerow({key: (format_amount(row.amount) if key == "amount" else row.to_dict().get(key, "")) for key in FIELDS})')
    replace(state,"budgeter/cli.py",'"from .amounts import format_amount\n"' if False else 'from .amounts import format_amount', 'from .amounts import format_amount')
    put(5,"","request.md","""Replace transaction storage and persisted transaction amounts with integer cents. Keep decimal-formatted CLI and CSV output and migrate version-1 saves. Leave budget and savings-goal arithmetic unchanged for now.""")
    put(5,"","supersedes.json",json.dumps(["tests/hidden_2/test_stage2.py"],indent=2))
    put(5,"visible","test_stage5.py",'''from budgeter.model import Transaction
from budgeter.store import BudgetStore

def test_integer_cents_and_display_boundary():
    row=Transaction("a","2026-01-01","1.23","food")
    assert row.amount_cents==123 and str(row.amount)=="1.23"

def test_new_json_schema_stores_cents(tmp_path):
    s=BudgetStore(tmp_path/"b.json"); s.add(Transaction("a","2026-01-01","1.23","food")); s.save()
    text=s.path.read_text()
    assert '"amount_cents": 123' in text and '"amount"' not in text
''')
    put(5,"hidden","test_stage5.py",'''from budgeter.model import Transaction
from budgeter.store import BudgetStore

def test_v1_migration_and_exact_cents():
    data={"version":1,"transactions":[
      {"transaction_id":"a","day":"2026-01-01","amount":"0.10","category":"food"},
      {"transaction_id":"b","day":"2026-01-01","amount":"0.20","category":"food"}]}
    s=BudgetStore.from_payload("unused",data)
    assert [r.amount_cents for r in s.transactions]==[10,20]
    s.add(Transaction("c","2026-01-01","0.30","food"))
    assert sum(r.amount_cents for r in s.transactions)==60
''')
    put(5,"","supersedes.json",json.dumps(["tests/hidden_2/test_stage2.py"],indent=2))
    write_patch(5,files,state)
    files=state.copy()

    # Stage 6 persistent invariant and AST check.
    for name, source in stage6_modules.items():
        state[name] = source
    store_cents = state["budgeter/store.py"]
    replace_text = lambda source, old, new: source.replace(old,new)
    store_cents = replace_text(store_cents,"    VERSION = 2","    VERSION = 3")
    store_cents = replace_text(store_cents,
        'if data.get("version") not in {1, cls.VERSION}:',
        'if data.get("version") not in {1, 2, cls.VERSION}:')
    store_cents = replace_text(store_cents,
        '"goals": [{"goal_id":g.goal_id,"name":g.name,"target":str(g.target),"saved":str(g.saved)} for g in self.goals]',
        '"goals": [goal.to_dict() for goal in self.goals]')
    store_cents = replace_text(store_cents,
        'store.goals = [SavingsGoal(**row) for row in data.get("goals", [])]',
        'store.goals = [SavingsGoal.from_dict(row) for row in data.get("goals", [])]')
    store_cents = replace_text(store_cents,
        '"budgets": dict(self.budgets),',
        '"budgets": {key:int(value) for key,value in self.budgets.items()},')
    store_cents = replace_text(store_cents,
        '        store.budgets = dict(data.get("budgets", {}))',
        '        raw_budgets=data.get("budgets", {}) or {}\n'
        '        store.budgets={key:(int(value) if data.get("version")==cls.VERSION else int(parse_amount(value)*100)) for key,value in raw_budgets.items()}')
    store_cents = replace_text(store_cents,
        'from .model import SavingsGoal, Transaction, validate_transaction_ids',
        'from .amounts import parse_amount\nfrom .model import SavingsGoal, Transaction, validate_transaction_ids')
    state["budgeter/store.py"] = store_cents
    stage6_modules["budgeter/store.py"] = store_cents
    put(6,"","request.md","""Global constraint G6.1: all financial arithmetic and stored monetary values use integer cents. Convert only at explicit input/display boundaries. Preserve this invariant in later stages.""")
    put(6,"","static_checks.py",'''import ast
from pathlib import Path

def test_financial_arithmetic_avoids_float_literals():
    root=Path(__file__).resolve().parents[1]/"budgeter"
    for name in ("summary.py","budgets.py","goals.py"):
        tree=ast.parse((root/name).read_text())
        for node in ast.walk(tree):
            assert not (isinstance(node,ast.Constant) and isinstance(node.value,float)),name
            assert not (isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=="float"),name
''')
    put(6,"visible","test_stage6.py",'''from budgeter.model import Transaction

def test_amount_state_is_an_integer():
    row=Transaction("a","2026-01-01","2.34","food")
    assert isinstance(row.amount_cents,int) and row.amount_cents==234
''')
    put(6,"hidden","test_stage6.py",'''from budgeter.budgets import CategoryBudgets
from budgeter.goals import add_goal, contribute

def test_budget_and_goal_state_use_integer_cents():
    budgets=CategoryBudgets(); budgets.set_limit("food","2026-01","1.25")
    assert budgets.payload()["food|2026-01"]==125
    goal=add_goal([],"g","Reserve","2.00")
    contribute(goal,"0.30")
    assert goal.target_cents==200 and goal.saved_cents==30
''')
    write_patch(6,files,state)
    files=state.copy()

    # Stage 7 fixes malformed optional storage data and implements deferred recurrence.
    put(7,"","supersedes.json",json.dumps(["tests/hidden_3/test_stage3_deferred.py"],indent=2))
    add(state,"budgeter/recurrence.py",'''from calendar import monthrange
from datetime import date
from .model import Transaction

def _month_shift(day,offset):
    index=day.year*12+day.month-1+offset
    year,month=divmod(index,12); month+=1
    return date(year,month,min(day.day,monthrange(year,month)[1]))

def expand_recurring(template,start_month,end_month):
    sy,sm=map(int,start_month.split("-")); first=date(sy,sm,1)
    if end_month:
        ey,em=map(int,end_month.split("-")); last=date(ey,em,1)
    else: last=date(first.year+1,first.month,1)
    source=date.fromisoformat(template.day); output=[]; offset=0
    while offset<24:
        day=_month_shift(source,offset); month=date(day.year,day.month,1)
        if month<first: offset+=1; continue
        if month>last: break
        amount=template.amount
        output.append(Transaction(f"{template.transaction_id}:{day:%Y-%m}",day.isoformat(),
                                  amount,template.category,template.description,"monthly"))
        offset+=1
    return output
''')
    # Scenario reaches the existing malformed-data crash before importing the deferred module.
    put(7,"","scenario.py",'''import json, tempfile
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
''')
    put(7,"","request.md","""The supplied scripted run crashes while loading a valid save whose optional transaction collection is null. Use the log and `run_scenario` to fix the root cause. Also complete the item deferred in Stage 3 without asking for its details.""")
    put(7,"visible","test_stage7.py",'''from budgeter.model import Transaction
from budgeter.recurrence import expand_recurring

def test_month_end_is_clamped():
    row=Transaction("r","2026-01-31","10","housing")
    assert [x.day for x in expand_recurring(row,"2026-01","2026-03")] == ["2026-01-31","2026-02-28","2026-03-31"]
''')
    put(7,"hidden","test_stage7.py",'''from budgeter.model import Transaction
from budgeter.recurrence import expand_recurring

def test_recurrence_ids_are_stable_and_bounded():
    row=Transaction("r","2026-01-31","10","housing")
    a=expand_recurring(row,"2026-01","2026-03")
    b=expand_recurring(row,"2026-01","2026-03")
    assert [x.transaction_id for x in a]==[x.transaction_id for x in b]
    assert len(a)==3 and a[1].transaction_id=="r:2026-02"

def test_deferred_expansion_exists():
    assert callable(expand_recurring)
''')
    # Fix null collection load in the reference state.
    replace(state,"budgeter/store.py",'data.get("transactions", [])','(data.get("transactions") or [])')
    write_patch(7,files,state)
    files=state.copy()

    # Stage 8 integrates persistence, CSV, recurrence and reporting.
    replace(state,"budgeter/store.py",'        self.budgets: dict = {}\n','        self.budgets: dict = {}\n        self.recurring = []\n')
    replace(state,"budgeter/store.py",'                "budgets": {key:int(value) for key,value in self.budgets.items()},\n','                "budgets": {key:int(value) for key,value in self.budgets.items()},\n                "recurring": [row.to_dict() for row in self.recurring],\n')
    replace(state,"budgeter/store.py",'        store.budgets={key:(int(value) if data.get("version")==cls.VERSION else int(parse_amount(value)*100)) for key,value in raw_budgets.items()}\n','        store.budgets={key:(int(value) if data.get("version")==cls.VERSION else int(parse_amount(value)*100)) for key,value in raw_budgets.items()}\n        store.recurring = [Transaction.from_dict(row) for row in (data.get("recurring") or [])]\n')
    replace(state,"budgeter/csv_io.py",'FIELDS = ("transaction_id", "day", "amount", "category", "description")','FIELDS = ("transaction_id", "day", "amount", "category", "description", "recurring")')
    replace(state,"budgeter/summary.py",'def monthly_summary(rows,month,budgets=None,goals=None):','def monthly_summary(rows,month,budgets=None,goals=None,recurring=()):')
    replace(state,"budgeter/summary.py",'    selected=month_transactions(rows,month)\n','    selected=month_transactions(list(rows)+list(recurring),month)\n')
    put(8,"","request.md","""Integrate recurring transactions with CSV import/export, versioned JSON save/load, monthly summaries, category budgets, and savings goals. Round-trip then report must preserve results and must not expand a recurring row twice.""")
    put(8,"visible","test_stage8.py",'''from budgeter.model import Transaction
from budgeter.store import BudgetStore

def test_recurring_rows_round_trip(tmp_path):
    store=BudgetStore(tmp_path/"b.json")
    store.recurring=[Transaction("r:2026-01","2026-01-31","5","food",recurring="monthly")]
    store.save(); loaded=BudgetStore.load(store.path)
    assert loaded.recurring[0].amount_cents==500
''')
    put(8,"hidden","test_stage8.py",'''from budgeter.model import Transaction
from budgeter.recurrence import expand_recurring
from budgeter.store import BudgetStore

def test_recurring_round_trip_preserves_ids_and_cents(tmp_path):
    store=BudgetStore(tmp_path/"b.json")
    base=Transaction("rent","2026-01-31","10","housing")
    store.recurring=expand_recurring(base,"2026-01","2026-02")
    store.save(); loaded=BudgetStore.load(store.path)
    assert [r.transaction_id for r in loaded.recurring]==["rent:2026-01","rent:2026-02"]
    assert all(r.amount_cents==1000 for r in loaded.recurring)
''')
    write_patch(8,files,state)
    manifest={"project":"budget_planner","kind":"calibration","stages":8,
      "orientation_answers":{"q1":"budgeter.amounts.parse_amount","q2":["transaction_id","day","amount","category","description","recurring"],"q3":"YYYY-MM-DD","q4":"budgeter.summary.monthly_summary","q5":"budgeter.model.normalize_category","q6":1,"q7":"budgeter.csv_io.import_csv","q8":"summary"},
      "probes":[
       {"introduced":1,"retired":2,"tests":[f"Q{i}" for i in range(1,9)],"text_only":False,"requirement":"R1.1"},
       {"introduced":2,"retired":None,"tests":["tests/hidden_2/test_stage2.py::test_month_boundary_decision"],"text_only":True,"requirement":"R2.1"},
       {"introduced":2,"retired":5,"tests":["tests/hidden_2/test_stage2.py::test_budget_decimal_payload_contract"],"text_only":False,"requirement":"R2.2"},
       {"introduced":3,"retired":None,"tests":["tests/hidden_3/test_stage3.py::test_refund_reduces_actual_category_spend"],"text_only":True,"requirement":"R3.1"},
       {"introduced":3,"retired":7,"tests":["tests/hidden_3/test_stage3_deferred.py::test_recurring_expansion_is_still_deferred"],"text_only":True,"requirement":"R3.2"},
       {"introduced":4,"retired":None,"tests":["tests/hidden_4/test_stage4.py::test_zero_record_between_nonzero_records_keeps_order"],"text_only":False,"requirement":"R4.1"},
       {"introduced":5,"retired":None,"tests":["tests/hidden_5/test_stage5.py::test_v1_migration_and_exact_cents"],"text_only":False,"requirement":"R5.1"},
       {"introduced":6,"retired":None,"tests":["tests/hidden_6/test_stage6.py::test_budget_and_goal_state_use_integer_cents"],"text_only":False,"requirement":"G6.1"},
       {"introduced":7,"retired":None,"tests":["tests/hidden_7/test_stage7.py::test_recurrence_ids_are_stable_and_bounded","tests/hidden_7/test_stage7.py::test_deferred_expansion_exists"],"text_only":True,"requirement":"R3.2"},
       {"introduced":8,"retired":None,"tests":["tests/hidden_8/test_stage8.py::test_recurring_round_trip_preserves_ids_and_cents"],"text_only":False,"requirement":"R8.1"}]}
    (ROOT/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")


if __name__ == "__main__":
    main()
