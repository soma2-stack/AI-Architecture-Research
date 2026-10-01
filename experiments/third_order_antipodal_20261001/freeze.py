"""Final pre-official content freeze. No certification is run here."""
import sys,json,hashlib,subprocess
sys.dont_write_bytecode=True
from pathlib import Path
ROOT=Path(__file__).resolve().parent; REPO=ROOT.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
old=ROOT.parent/'antipodal_robust_dimension_20261001'
archive=json.loads((old/'BYTE_EXACT_ARCHIVE.json').read_text())
assert all(sha(old/name)==h for name,h in archive['sha256'].items())
sources=[
    old/'antipodal_kernel.py',old/'screen_proxy.py',old/'BYTE_EXACT_ARCHIVE.json',
    old/'stage2_proxy/outputs/independent_n4_confirmation_query_r6_s2.json']
sources += [ROOT.parent/'robust_witness_search_20261001'/name for name in ('cpu_jets.py','interval.py','certificate_kernel.py','config.json')]
sources += [ROOT.parent/'robust_certificate_tightness_20261001/inputs.json']
data={'parent_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip(),
      'meaning':'New method/candidate freeze before any official box evaluation; prior numerical proxy disclosed',
      'local_sha256':{p.name:sha(p) for p in sorted(ROOT.iterdir()) if p.is_file() and p.name!='FROZEN.json'},
      'source_sha256':{str(p.relative_to(REPO)).replace('\\','/'):sha(p) for p in sources}}
assert json.loads((ROOT/'development_tests.json').read_text())['passed']
assert not (ROOT/'result.json').exists()
(ROOT/'FROZEN.json').write_text(json.dumps(data,indent=2))
print('Setup frozen; official results absent; old evidence unchanged')
