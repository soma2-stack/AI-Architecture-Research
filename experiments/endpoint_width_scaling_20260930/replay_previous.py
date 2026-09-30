"""Recheck previous certificates without writing in their directory."""
import core as c
import json,hashlib
from verify import verify
meter=c.Meter('Read-only replay of five previous width2 certificates')
c.ACTIVE_METER=meter
try:
    old=c.ROOT.parent/'endpoint_certificate_20260930'
    paths=sorted(old.glob('certificate_*.json'));assert len(paths)==5
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in old.iterdir() if p.is_file()}
    records=[]
    for path in paths:
        meter.check();record=verify(json.loads(path.read_text()));records.append({'file':str(path),**record})
        print(path.name,record['verified'],flush=True)
    assert hashes=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in old.iterdir() if p.is_file()}
    (c.ROOT/'previous_replay.json').write_text(json.dumps({'old_files_unchanged':True,'hashes':hashes,'certificates':records},indent=2))
finally:meter.finish()
