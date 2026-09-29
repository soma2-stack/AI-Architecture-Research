import ast
from pathlib import Path

def test_global_random_import_is_confined_to_rng_module():
    package = Path(__file__).parents[1] / "deckgame"
    offenders = []
    for path in package.glob("*.py"):
        if path.name == "rng.py":
            continue
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import) and any(alias.name == "random" for alias in node.names):
                offenders.append(path.name)
            if isinstance(node, ast.ImportFrom) and node.module == "random":
                offenders.append(path.name)
    assert offenders == []
