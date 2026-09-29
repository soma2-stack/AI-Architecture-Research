import json

import pytest

from expr import Environment, evaluate
from expr.builtins import invoke
from expr.cli import run_lines
from expr.errors import EvalError, LexError, ParseError
from expr.format import diagnostic, number
from expr.inspect import called_functions, dependency_order, editor_summary, inspect, max_depth, node_count, unresolved_names, variable_reads, variable_writes
from expr.lexer import tokenize
from expr.parser import parse
from expr.session import Session


def test_empty_program():
    assert evaluate("") is None


def test_multi_statement_returns_last():
    assert evaluate("a=2;b=a+3;b*2") == 10


def test_environment_history():
    env = Environment()
    evaluate("a=1;a=2", env)
    assert env.history == [("a", 1.0), ("a", 2.0)]


def test_environment_reset():
    env = Environment()
    evaluate("a=1", env)
    env.reset()
    assert env.values == {}


def test_modulo_zero():
    with pytest.raises(EvalError, match="modulo by zero"):
        evaluate("1%0")


def test_builtin_abs():
    assert evaluate("abs(-4)") == 4


def test_builtin_round():
    assert evaluate("round(1.234,2)") == 1.23


def test_builtin_bad_arity():
    with pytest.raises(EvalError, match="one argument"):
        evaluate("abs(1,2)")


def test_builtin_unknown():
    with pytest.raises(EvalError, match="unknown function"):
        evaluate("mystery(2)")


def test_number_format_int():
    assert number(3.0) == "3"


def test_number_format_decimal():
    assert number(0.25) == "0.25"


def test_diagnostic_marks_character():
    text = diagnostic("1 @ 2", LexError("bad", 2))
    assert text.endswith("  ^")


def test_session_roundtrip():
    s = Session()
    assert s.execute("a=2") == "2"
    assert s.execute("a*3") == "6"
    restored = Session.deserialize(s.serialize())
    assert restored.env.values == {"a": 2.0}
    assert restored.outputs == ["2", "6"]


def test_session_version_check():
    data = json.loads(Session().serialize())
    data["version"] = 999
    with pytest.raises(ValueError):
        Session.deserialize(json.dumps(data))


def test_cli_lines_keep_environment():
    assert list(run_lines(["a=2", "a+1"])) == ["2", "3"]


def test_cli_reports_error_without_stopping():
    output = list(run_lines(["1/0", "2+3"]))
    assert "division by zero" in output[0] and output[1] == "5"


def test_inspect_variables():
    assert variable_reads("a=2;b=a+3") == {"a"}
    assert variable_writes("a=2;b=a+3") == {"a", "b"}


def test_inspect_calls():
    assert called_functions("max(1,min(2,3))") == {"max", "min"}


def test_inspect_counts():
    assert node_count("1+2") == 4
    assert max_depth("1+2") == 3


def test_inspection_record():
    row = inspect("x=mean(2,4);x+1")
    assert row.nodes > 4 and row.calls == frozenset({"mean"})
    assert row.writes == frozenset({"x"})


def test_unresolved_detected():
    assert unresolved_names("a=b+1;c=a+2", set()) == {"b"}


def test_unresolved_respects_defined():
    assert unresolved_names("a=b+1", {"b"}) == set()


def test_dependency_order():
    assert dependency_order("a=b+1;c=a+2") == [
        ("a", frozenset({"b"})), ("c", frozenset({"a"}))]


def test_editor_summary():
    row = editor_summary("a=b+1", {"b"})
    assert row["unresolved"] == [] and row["writes"] == ["a"]
