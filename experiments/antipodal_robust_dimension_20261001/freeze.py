"""Write FROZEN.json: hashes of protocol, code, candidates, charts, screening outputs, derived caches and reviewed sources."""
import json, hashlib, datetime
from pathlib import Path
ROOT = Path(__file__).parent
files = ['PREREGISTRATION.md', 'PROOF.md', 'config.json', 'antipodal_kernel.py', 'certify_official.py', 'make_candidates.py',
         'jets_cache.py', 'screen_proxy.py', 'screen_search.py', 'test_kernel_reproduction.py', 'test_kernel_reproduction.json',
         'candidates.json', 'freeze.py']
files += sorted(p.relative_to(ROOT).as_posix() for d in ('charts', 'screening') for p in (ROOT/d).glob('*.json'))
files += sorted(p.relative_to(ROOT).as_posix() for p in (ROOT/'cache').glob('JI_*.json'))
files += ['../robust_witness_search_20261001/certificate_kernel.py', '../robust_witness_search_20261001/cpu_jets.py',
          '../robust_witness_search_20261001/interval.py', '../robust_certificate_tightness_20261001/inputs.json']
assert len(list((ROOT/'cache').glob('JI_*.json'))) == 16
sha = {f: hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files}
(ROOT/'FROZEN.json').write_text(json.dumps({'stage': 'stage-1 pre-official freeze (no official certificate computed yet)',
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'files': len(sha), 'sha256': sha}, indent=1)+'\n')
print('frozen', len(sha), 'files')
