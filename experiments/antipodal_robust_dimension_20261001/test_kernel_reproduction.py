"""Kernel reproduction test: on the reviewed 4D chart the copied steps must reproduce the stored certificate exactly."""
import sys, json
sys.dont_write_bytecode = True
from fractions import Fraction as Q
from pathlib import Path
import antipodal_kernel as k
SRC = k.REPO/'experiments/support_aware_robust_dimension_20261001'
res = json.loads((SRC/'result_independent_n4_confirmation.json').read_text())
case = next(c for c in k.INPUT['cases'] if c['name'] == 'independent_n4_confirmation')
cert = res['certificate']; r = cert['r']
B = [[Q(v) for v in row] for row in res['frame']['B']]
L = [[Q(v) for v in row] for row in cert['selected_projection']]
base = k.base_for(case, B, 192)
out, cap = k.certify_antipodal(base, [Q(1, 8)]*r, Q(1, 8), L)
checks = {'K_hidden': out['K_hidden'] == cert['K_hidden'], 'K_selected': out['K_selected'] == cert['K_selected'],
          'eta_hidden': out['eta_hidden'] == cert['eta_hidden'],
          'scaled_E': out['scaled_jacobian_residual_upper'] == cert['scaled_jacobian_residual_upper'],
          'Gamma': out['normal_first_derivative_upper'] == cert['normal_first_derivative_upper'],
          'eta_global': out['eta_global_upper'] == cert['eta_sensitivity']}
import numpy as np
bb = np.load(SRC/'best_bounds_independent_n4_confirmation_192.npz')
checks['HH'] = bool(np.array_equal(bb['HH'], cap['HH'])); checks['HS'] = bool(np.array_equal(bb['HS'], cap['HS']))
print(json.dumps(checks)); print('beta_i', [float(Q(x)) for x in out['beta_i']], 'certified', out['certified_dimension'])
assert all(checks.values())
Path(ROOT := k.ROOT, 'test_kernel_reproduction.json').write_text(json.dumps({'checks': checks, 'beta_i': out['beta_i'], 'passed': True}, indent=1))
