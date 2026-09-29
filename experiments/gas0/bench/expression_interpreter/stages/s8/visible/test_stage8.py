import json
from expr.cli import run_lines

def test_json_error_mode_and_success_output():
    rows=list(run_lines(["1/0","2+3"],json_errors=True))
    assert json.loads(rows[0])["error"] == "division by zero"
    assert rows[1] == "5"
