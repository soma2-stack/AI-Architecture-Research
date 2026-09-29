import ast
from pathlib import Path

def test_interpreter_never_calls_host_eval_or_exec():
    root=Path(__file__).resolve().parents[1]/"expr"
    for path in root.glob("*.py"):
        tree=ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            assert not (isinstance(node,ast.Call) and isinstance(node.func,ast.Name)
                        and node.func.id in {"eval","exec"}),path.name
