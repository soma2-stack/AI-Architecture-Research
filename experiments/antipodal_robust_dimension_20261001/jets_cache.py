"""Derived cache: reviewed cpu_jets interval Jacobian at each frozen endpoint (no new mathematics)."""
import sys, json, hashlib
sys.dont_write_bytecode = True
from fractions import Fraction as Q
import antipodal_kernel as k
name, bits = sys.argv[1], int(sys.argv[2])
case = next(c for c in k.INPUT['cases'] if c['name'] == name)
k.I.precision(bits); m = k.model(case); X = [[Q(v) for v in row] for row in case['X']]
_, JI, _ = k.c.jets(m, X, 'interval')
data = {'name': name, 'bits': bits, 'shape': list(JI.shape), 'lo': [[x.lo for x in row] for row in JI.tolist()], 'hi': [[x.hi for x in row] for row in JI.tolist()]}
(k.ROOT/'cache').mkdir(exist_ok=True); p = k.ROOT/f'cache/JI_{name}_{bits}.json'; p.write_text(json.dumps(data))
print(name, bits, hashlib.sha256(p.read_bytes()).hexdigest()[:16], flush=True)
