"""REPAIR runner (see IMPLEMENTATION_REPAIRS.md). Official stage-1 certification of ONE frozen candidate at 192 bits, then 256-bit regeneration (frozen K, K_h)."""
import sys, json, hashlib, time, traceback
sys.dont_write_bytecode = True
from fractions import Fraction as Q
import numpy as np
import antipodal_kernel as k
ROOT = k.ROOT
frozen = json.loads((ROOT/'FROZEN.json').read_text())
for name, h in frozen['sha256'].items(): assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == h, name
cid = sys.argv[1]; cands = {c['id']: c for c in json.loads((ROOT/'candidates.json').read_text())}; cand = cands[cid]
chart = json.loads((ROOT/f"charts/{cand['chart']}.json").read_text()); case = next(c for c in k.INPUT['cases'] if c['name'] == cand['name'])
n = case['n']; r = cand['r']
B = [[Q(v) for v in row[:n+r]] for row in chart['B']]; L = [[Q(v) for v in row] for row in chart['L'][:r]]
aa = [Q(v) for v in cand['a']]; ah = Q(cand['ah'])
def JI(bits):
    d = json.loads((ROOT/f"cache/JI_{cand['name']}_{bits}.json").read_text())
    k.I.precision(bits)
    return np.array([[k.I(lo, hi, True) for lo, hi in zip(rl, rh)] for rl, rh in zip(d['lo'], d['hi'])], dtype=object)
t0 = time.time(); row = {'id': cid, 'candidate': cand}
try:
    base = k.base_for(case, B, 192, JI(192))
    ret = k.certify_antipodal(base, aa, ah, L); out, cap = ret if isinstance(ret, tuple) else (ret, None)  # REPAIR: early-return path returns a bare dict
    row['result_192'] = out; row['seconds_192'] = time.time()-t0; row['runner'] = 'certify_official_repair.py'
    if cap is not None: np.savez_compressed(ROOT/f'results/curvature_{cid}_192.npz', **cap)
    if out.get('all_faces_exceed_epsilon'):
        frozenK = ([[Q(x) for x in r_] for r_ in out['K_hidden']], [[Q(x) for x in r_] for r_ in out['K_selected']])
        high = k.base_for(case, B, 256, JI(256))
        ret2 = k.certify_antipodal(high, aa, ah, L, frozen=frozenK); out2, cap2 = ret2 if isinstance(ret2, tuple) else (ret2, None); row['result_256'] = out2
        if cap2 is not None: np.savez_compressed(ROOT/f'results/curvature_{cid}_256.npz', **cap2)
        row['certified_dimension'] = r if out2.get('all_faces_exceed_epsilon') else None
    else: row['certified_dimension'] = None
except Exception:
    row['error'] = traceback.format_exc()
row['seconds_total'] = time.time()-t0
(ROOT/f'results/{cid}.json').write_text(json.dumps(row, indent=1))
print(cid, 'r', r, 'certified', row.get('certified_dimension'), 'weakest', row.get('result_192', {}).get('weakest_beta') and float(Q(row['result_192']['weakest_beta'])), '%.0fs' % row['seconds_total'], flush=True)
