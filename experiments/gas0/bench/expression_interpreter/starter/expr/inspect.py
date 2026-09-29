"""Read-only AST inspection for editor hints and static diagnostics."""
from __future__ import annotations

from dataclasses import dataclass

from .nodes import Assign, Binary, Call, Name, Number, Program, Unary
from .parser import parse


def children(node) -> tuple:
    if isinstance(node, Program):
        return node.statements
    if isinstance(node, Assign):
        return (node.value,)
    if isinstance(node, Binary):
        return (node.left, node.right)
    if isinstance(node, Unary):
        return (node.operand,)
    if isinstance(node, Call):
        return node.arguments
    if isinstance(node, (Name, Number)):
        return ()
    raise TypeError(type(node))


def walk(node):
    yield node
    for child in children(node):
        yield from walk(child)


def node_count(source: str) -> int:
    return sum(1 for _ in walk(parse(source)))


def max_depth(source: str) -> int:
    def depth(node):
        nested = children(node)
        return 1 + max((depth(child) for child in nested), default=0)
    return depth(parse(source))


def variable_reads(source: str) -> set[str]:
    return {node.identifier for node in walk(parse(source)) if isinstance(node, Name)}


def variable_writes(source: str) -> set[str]:
    return {node.identifier for node in walk(parse(source)) if isinstance(node, Assign)}


def called_functions(source: str) -> set[str]:
    return {node.callee for node in walk(parse(source)) if isinstance(node, Call)}


@dataclass(frozen=True)
class Inspection:
    nodes: int
    depth: int
    reads: frozenset[str]
    writes: frozenset[str]
    calls: frozenset[str]


def inspect(source: str) -> Inspection:
    tree = parse(source)
    all_nodes = list(walk(tree))

    def depth(node):
        return 1 + max((depth(child) for child in children(node)), default=0)

    return Inspection(
        nodes=len(all_nodes),
        depth=depth(tree),
        reads=frozenset(n.identifier for n in all_nodes if isinstance(n, Name)),
        writes=frozenset(n.identifier for n in all_nodes if isinstance(n, Assign)),
        calls=frozenset(n.callee for n in all_nodes if isinstance(n, Call)),
    )


def unresolved_names(source: str, defined: set[str]) -> set[str]:
    known = set(defined)
    unresolved = set()
    for statement in parse(source).statements:
        for node in walk(statement):
            if isinstance(node, Name) and node.identifier not in known:
                unresolved.add(node.identifier)
        if isinstance(statement, Assign):
            known.add(statement.identifier)
    return unresolved


def dependency_order(source: str) -> list[tuple[str, frozenset[str]]]:
    """Assignments paired with reads needed before each write."""
    rows = []
    for statement in parse(source).statements:
        if not isinstance(statement, Assign):
            continue
        reads = frozenset(node.identifier for node in walk(statement.value)
                          if isinstance(node, Name))
        rows.append((statement.identifier, reads))
    return rows


def editor_summary(source: str, defined: set[str] | None = None) -> dict:
    """Produce JSON-ready static hints without evaluating the source."""
    row = inspect(source)
    return {
        "nodes": row.nodes,
        "depth": row.depth,
        "reads": sorted(row.reads),
        "writes": sorted(row.writes),
        "calls": sorted(row.calls),
        "unresolved": sorted(unresolved_names(source, set(defined or ()))),
        "assignment_dependencies": [(name, sorted(deps))
                                    for name, deps in dependency_order(source)],
    }
