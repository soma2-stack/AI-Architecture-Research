import json
from expr.cli import main

def test_cli_flag_formats_each_error_line(tmp_path,capsys,monkeypatch):
    path=tmp_path/"program.expr"; path.write_text("1/0\n4+1\n")
    assert main(["--file",str(path),"--json-errors"])==0
    output=capsys.readouterr().out.splitlines()
    assert json.loads(output[0])["position"]==1
    assert output[1]=="5"
