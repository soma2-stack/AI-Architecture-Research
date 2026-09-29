# req: R6.1
import ast
from pathlib import Path

def test_no_raw_event_append_outside_world():
    root = Path(__file__).resolve().parents[1] / 'arena'
    for path in root.glob('*.py'):
        if path.name == 'model.py':
            continue
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                assert not (node.func.attr == 'append' and
                            isinstance(node.func.value, ast.Attribute) and
                            node.func.value.attr == 'events'), str(path)
