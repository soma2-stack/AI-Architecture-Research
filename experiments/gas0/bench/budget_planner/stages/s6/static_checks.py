import ast
from pathlib import Path

def test_financial_arithmetic_avoids_float_literals():
    root=Path(__file__).resolve().parents[1]/"budgeter"
    for name in ("summary.py","budgets.py","goals.py"):
        tree=ast.parse((root/name).read_text())
        for node in ast.walk(tree):
            assert not (isinstance(node,ast.Constant) and isinstance(node.value,float)),name
            assert not (isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=="float"),name
