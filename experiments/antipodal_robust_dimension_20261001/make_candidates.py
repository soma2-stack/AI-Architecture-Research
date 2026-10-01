"""Build the frozen candidate list from screening outputs (rule fixed in PREREGISTRATION.md)."""
import json, glob, math
from fractions import Fraction as Q
from pathlib import Path
import numpy as np
from screen_proxy import Endpoint
ROOT = Path(__file__).parent
dy = lambda x: str(Q(round(float(x)*2**128), 2**128))
down = lambda x: str(Q(math.floor(float(x)*2**20), 2**20))
rows = [json.load(open(f)) for f in sorted(glob.glob(str(ROOT/'screening/*.json')))]
cands = []; charts = {}; eps = {}
for x in rows:
    if x.get('score', -1) < 1.0: continue
    key = f"{x['name']}_{x['basis']}_r{x['r']}"
    if key not in charts:
        ep = eps.get(x['name']) or eps.setdefault(x['name'], Endpoint(x['name']))
        B, U, s = ep.basis(x['basis'], x['r']); L = ep.projection(U)
        charts[key] = {'B': [[dy(v) for v in row] for row in B], 'L': [[dy(v) for v in row] for row in L]}
    cands.append({'id': f"{key}_s{x['seed']}", 'name': x['name'], 'basis': x['basis'], 'r': x['r'], 'seed': x['seed'], 'chart': key,
                  'a': [down(v) for v in x['a']], 'ah': down(x['ah']), 'proxy_score': x['score']})
# control: reviewed 4D chart (support-aware experiment result), same B/L/amplitudes
SRC = ROOT.parents[0]/'support_aware_robust_dimension_20261001/result_independent_n4_confirmation.json'
res = json.loads(SRC.read_text()); cert = res['certificate']
charts['control_reviewed_4D'] = {'B': res['frame']['B'], 'L': cert['selected_projection']}
cands.append({'id': 'control_reviewed_4D', 'name': 'independent_n4_confirmation', 'basis': 'reviewed', 'r': 4, 'seed': 0,
              'chart': 'control_reviewed_4D', 'a': ['1/8']*4, 'ah': '1/8', 'proxy_score': None})
(ROOT/'charts').mkdir(exist_ok=True)
for key, ch in charts.items(): (ROOT/f'charts/{key}.json').write_text(json.dumps(ch))
(ROOT/'candidates.json').write_text(json.dumps(cands, indent=1))
print(len(cands), 'candidates;', len(charts), 'charts')
