from taskapp.atomic import atomic_write_text

def test_atomic_writer_replaces_complete_content(tmp_path):
    path=tmp_path/"state.json"; path.write_text("old")
    atomic_write_text(path,"new")
    assert path.read_text()=="new" and not path.with_name("state.json.tmp").exists()
