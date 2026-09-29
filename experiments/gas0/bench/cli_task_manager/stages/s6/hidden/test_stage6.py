from taskapp.atomic import atomic_write_text

def test_atomic_writer_creates_parent_and_keeps_utf8(tmp_path):
    path=tmp_path/"nested"/"state.json"
    atomic_write_text(path,'{"title":"café"}')
    assert path.read_text(encoding="utf-8")=='{"title":"café"}'
