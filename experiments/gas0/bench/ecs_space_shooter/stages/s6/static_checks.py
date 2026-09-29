import ast
from pathlib import Path

def test_allocator_has_no_free_list_reuse():
    package = Path(__file__).parents[1] / "spaceecs"
    tree = ast.parse((package / "model.py").read_text())
    reused = [node for node in ast.walk(tree)
              if isinstance(node, ast.Attribute) and node.attr == "free_ids"]
    assert reused == []
    source = (package / "model.py").read_text()
    allocator = source.split("def create_entity", 1)[1].split("def remove_entity", 1)[0]
    assert "next_entity_id" in allocator
