import ast
from pathlib import Path

def test_random_draws_are_owned_by_seeded_rng():
    root=Path(__file__).resolve().parents[1]/"rogue"
    for path in root.glob("*.py"):
        tree=ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute):
                if isinstance(node.func.value,ast.Name) and node.func.value.id=="random":
                    assert path.name=="rng.py" and node.func.attr=="Random",path.name
