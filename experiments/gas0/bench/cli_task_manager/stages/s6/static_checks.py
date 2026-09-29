import ast
from pathlib import Path

def test_persistent_store_uses_atomic_replacement():
    root=Path(__file__).resolve().parents[1]/"taskapp"
    tree=ast.parse((root/"store.py").read_text(encoding="utf-8"))
    calls={node.func.id for node in ast.walk(tree) if isinstance(node,ast.Call) and isinstance(node.func,ast.Name)}
    assert "atomic_write_text" in calls
    assert "write_text" not in calls
