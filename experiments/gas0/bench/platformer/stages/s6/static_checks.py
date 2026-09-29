import ast
from pathlib import Path

def test_world_frame_path_uses_fixed_point():
    root=Path(__file__).resolve().parents[1]/"platformer"
    tree=ast.parse((root/"world.py").read_text(encoding="utf-8"))
    calls={node.func.id for node in ast.walk(tree) if isinstance(node,ast.Call) and isinstance(node.func,ast.Name)}
    assert "step_fixed_body" in calls and "step_body" not in calls
