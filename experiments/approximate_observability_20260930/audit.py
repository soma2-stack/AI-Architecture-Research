"""Conditioning audit at archived witnesses. No optimizer or GPU API is used."""
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
for _key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[_key] = '1'
import atexit
import hashlib
import json
import math
import sys
import time
from fractions import Fraction as Q
from pathlib import Path
import mpmath as mp
import numpy as np
import psutil

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
CFG = json.loads((ROOT / 'config.json').read_text())
sys.path.insert(0, str(REPO / 'experiments/endpoint_width_scaling_20260930'))
import core as archived  # Read-only Model/jets; ACTIVE_METER stays None.
import ctypes
def limit_loaded_blas():
    records = []
    for mapping in psutil.Process().memory_maps():
        if 'openblas' not in mapping.path.lower():
            continue
        dll = ctypes.CDLL(mapping.path)
        for prefix, suffix in (('scipy_openblas_', '64_'), ('scipy_openblas_', ''),
                               ('openblas_', '64_'), ('openblas_', '')):
            try:
                setter = getattr(dll, prefix+'set_num_threads'+suffix)
                getter = getattr(dll, prefix+'get_num_threads'+suffix)
            except AttributeError:
                continue
            setter.argtypes = [ctypes.c_int]
            setter.restype = None
            getter.restype = ctypes.c_int
            setter(1)
            records.append({'library': mapping.path, 'threads': getter()})
            break
    assert records and all(p['threads'] == 1 for p in records)
    return records
THREAD_POOLS = limit_loaded_blas()

class Meter:
    def __init__(self, label):
        self.label = label
        self.process = psutil.Process()
        self.start = time.perf_counter()
        self.closed = False
        self.prior = sum(r['cpu_seconds'] for r in read_jsonl(ROOT / 'cpu_ledger.jsonl'))
        atexit.register(self.finish)
    def check(self):
        assert self.prior + time.process_time() < CFG['cpu_cap_seconds'] - CFG['stop_margin_seconds'], 'CPU budget stop'
        assert self.process.memory_info().rss < CFG['rss_cap_bytes'], 'RAM budget stop'
    def finish(self):
        if self.closed:
            return
        self.closed = True
        info = self.process.memory_info()
        row = {'label': self.label, 'cpu_seconds': time.process_time(),
               'wall_seconds': time.perf_counter() - self.start,
               'peak_rss_bytes': max(info.rss, getattr(info, 'peak_wset', info.rss)),
               'gpu_used': False, 'cuda_build': archived.torch.version.cuda,
               'device': 'cpu', 'workers': 1}
        append_jsonl(ROOT / 'cpu_ledger.jsonl', row)
        return row

def read_jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

def append_jsonl(path, row):
    with path.open('a', encoding='utf-8') as handle:
        handle.write(json.dumps(row) + '\n')

def cast(q):
    q = Q(q)
    return mp.mpf(q.numerator) / q.denominator

def text_number(x):
    return mp.nstr(x, 65)

def spectrum(A):
    return list(mp.svd(A, compute_uv=False))

def report_spectrum(values):
    return {'values': [text_number(x) for x in values],
            'largest': text_number(values[0]), 'smallest': text_number(values[-1]),
            'condition': text_number(values[0] / values[-1]) if values[-1] else 'Infinity',
            'absolute_counts': {str(t): sum(x >= mp.mpf(str(t)) for x in values) for t in CFG['absolute_thresholds']},
            'relative_counts': {str(t): sum(x >= values[0] * mp.mpf(str(t)) for x in values) for t in CFG['absolute_thresholds']}}

def certificate_matrix(data):
    denominator = mp.mpf(2) ** (data['bits'] + 1)
    return mp.matrix([[(mp.mpf(lo) + mp.mpf(hi)) / denominator for lo, hi in row]
                      for row in data['J_intervals']])

def fixed_h_matrix(J, n):
    # Full orthonormal Q: remaining columns are a basis of the history kernel.
    Jh = J[:n, :]
    QQ, RR = mp.qr(Jh.T)
    N = QQ[:, n:]
    defect = mp.norm(Jh * N)
    assert defect < mp.mpf('1e-65'), f'Null projection defective: {defect}'
    return J[n:, :] * N, N, defect

def parameter_scales(model):
    scale = {}
    for name in ('R', 'W', 'b'):
        values = [cast(model.params[p]) for p, (_, _, group, _) in enumerate(model.meta) if group == name]
        scale[name] = mp.sqrt(sum(x * x for x in values) / len(values))
        assert scale[name] > 0
    return scale

def scaled_sensitivity_matrix(A, model):
    scales = parameter_scales(model)
    input_sd = mp.sqrt(mp.mpf(3) / 32)
    return mp.matrix([[A[i, j] * scales[model.meta[p][2]] * input_sd for j in range(A.cols)]
                      for i, (_, p) in enumerate(model.support)])

def head_bounds(model):
    n = model.n
    R = mp.zeros(n)
    W = mp.zeros(n)
    for i, j, p in model.layers[0]['R']:
        R[i, j] = cast(model.params[p])
    for i, j, p in model.layers[0]['W']:
        W[i, j] = cast(model.params[p])
    rsv, wsv = spectrum(R), spectrum(W)
    beta = max(mp.mpf(1), mp.sqrt(sum(x*x for x in R)))
    qmin = 1 / mp.sqrt(n)
    alpha = rsv[-1] * wsv[-1] * 2 * qmin * mp.sech(mp.mpf(3)/4)**2 * mp.tanh(mp.mpf(1)/4) / beta
    gamma_margin = (mp.sech(mp.mpf(1)/4)**2 - mp.sech(mp.mpf(3)/4)**2) / 2
    ball_radius = rsv[-1] * qmin * gamma_margin / beta
    return {'sigma_min_R': text_number(rsv[-1]), 'sigma_max_R': text_number(rsv[0]),
            'sigma_min_W': text_number(wsv[-1]), 'beta': text_number(beta),
            'alpha_lower_formula_value': text_number(alpha),
            'adjoint_ball_radius_formula_value': text_number(ball_radius),
            'rigor': 'Analytic inequalities rigorous; displayed singular-value constants numerical, not outward interval bounds.'}

def hessian_bounds(params, n, T, B):
    """Exact rational uniform D^2 F bound in input infinity norm.

    Separate directions are input u,v (infinity norm <=1), and one parameter
    coordinate. |tanh'|<=1, |tanh''|<=2, |tanh'''|<=4 globally.
    """
    a = max(sum(abs(params[i*n+j]) for j in range(n)) for i in range(n))
    w = max(sum(abs(params[n*n+i*n+j]) for j in range(n)) for i in range(n))
    H = max(Q(1), B)
    A = BB = C = D = E = Q(0)
    for _ in range(T):
        v = a*A + w
        v2 = a*BB
        z = a*C + H
        z1 = a*D + A + 1
        z2 = a*E + BB
        A, BB, C, D, E = v, 2*v*v+v2, z, 2*z*v+z1, 4*z*v*v+2*(z*v2+2*z1*v)+z2
    return max(BB, E), a, w

def certified_patch(data, n):
    # Use the accepted outward certificate; no accessibility proof is rerun.
    bits = data['bits']
    eta = Q(int(data['proof']['residual_infinity_numerator']), 1 << bits)
    assert data['proof']['verified'] and 0 <= eta < 1
    norm_M = max(sum(Q(abs(int(v)), 1 << bits) for v in row) for row in data['preconditioner'])
    params = [Q(p) for p in data['params']]
    B = max(abs(Q(v)) for row in data['X'] for v in row) + 1
    L, a, w = hessian_bounds(params, n, data['T'], B)
    r = min(Q(1), (1-eta) / (2*norm_M*L))
    kappa = eta + norm_M*L*r
    rho = (1-eta)*r / (2*norm_M)
    radius = rho / 2
    assert kappa < 1 and radius > 0
    out = {'eta_exact': str(eta), 'inverse_norm_infinity_exact': str(norm_M),
           'hessian_bound_exact': str(L), 'input_cube_radius_exact': str(r),
           'contraction_bound_exact': str(kappa), 'output_cube_radius_exact': str(rho),
           'fixed_h_frobenius_radius_exact': str(radius),
           'R_row_norm_exact': str(a), 'W_row_norm_exact': str(w),
           'fixed_h_frobenius_radius': text_number(cast(radius)),
           'log10_radius': text_number(mp.log10(cast(radius))),
           'meaning': 'Sufficient reachable ball around exact S(X0), NOT largest reachable ball or practical distortion threshold.'}
    return out

def model_at(data, n, independent=False):
    model = archived.Model('independent' if independent else 'dense', n)
    if independent:
        dense = [Q(x) for x in data['params']]
        for p, (_, i, group, j) in enumerate(model.meta):
            if group == 'W':
                model.params[p] = dense[n*n+i*n+j]
            elif group == 'b':
                model.params[p] = dense[2*n*n+i]
    else:
        model.params = [Q(x) for x in data['params']]
    return model

def prefix_diagnostics(model, X):
    results = []
    for T in (4, 8, len(X)):
        F, J, S = archived.jets(model, X[:T], 'float')
        QQ, _ = np.linalg.qr(J[:model.n].T, mode='complete')
        A = J[model.n:] @ QQ[:, model.n:]
        values = np.linalg.svd(A, compute_uv=False)
        results.append({'T': T, 'available_input_tangent_dimension': A.shape[1],
                        'sensitivity_coordinates': A.shape[0], 'values_float64': values.tolist(),
                        'counts_at_1e-3': int(sum(values >= 1e-3)),
                        'counts_at_1e-6': int(sum(values >= 1e-6)),
                        'note': 'Tangent/float64 diagnostic only; no rank or finite-radius claim.'})
    return results

def run(meter):
    assert archived.ACTIVE_METER is None
    hardware = archived.hardware()
    assert hardware['device'] == 'cpu'
    hardware['threadpools'] = THREAD_POOLS
    assert all(p['threads'] == 1 for p in hardware['threadpools'])
    source_paths = [REPO / x for x in CFG['dense_certificates'].values()]
    source_paths += [REPO / 'experiments/endpoint_width_scaling_20260930/core.py',
                     REPO / 'experiments/endpoint_width_scaling_20260930/interval.py']
    hashes = {str(p.relative_to(REPO)): hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths}
    results = []
    mp.mp.dps = CFG['precision_digits']
    for n in CFG['widths']:
        meter.check()
        data = json.loads((REPO / CFG['dense_certificates'][str(n)]).read_text())
        X = [[Q(v) for v in row] for row in data['X']]
        for independent in (False, True):
            meter.check()
            case = 'independent' if independent else 'dense'
            print(f'{case} n={n}: started', flush=True)
            begin = time.process_time()
            model = model_at(data, n, independent)
            before = model.serialize()
            if independent:
                F, JJ, S = archived.jets(model, X, 'mp')
                J = mp.matrix(JJ.tolist())
            else:
                J = certificate_matrix(data)
            A, N, defect = fixed_h_matrix(J, n)
            full_values = spectrum(J)
            raw_values = spectrum(A)
            normalized_values = spectrum(scaled_sensitivity_matrix(A, model))
            row = {'case': case, 'n': n, 'P': model.P, 'T': len(X),
                   'full_sensitivity_coordinates': n*model.P,
                   'structurally_allowed_sensitivity_coordinates': len(model.support),
                   'fixed_h_history_tangent_dimension': N.cols, 'null_projection_defect': text_number(defect),
                   'endpoint_raw': report_spectrum(full_values),
                   'fixed_h_raw': report_spectrum(raw_values),
                   'fixed_h_input_sd_relative_parameter': report_spectrum(normalized_values),
                   'parameter_block_RMS': {k: text_number(v) for k, v in parameter_scales(model).items()},
                   'future_head': head_bounds(model), 'prefixes': prefix_diagnostics(model, X),
                   'params_hash': hashlib.sha256(json.dumps(model.serialize()).encode()).hexdigest(),
                   'input_hash': hashlib.sha256(json.dumps(data['X']).encode()).hexdigest()}
            if not independent:
                row['reachable_patch'] = certified_patch(data, n)
            if n == 4 and not independent:
                meter.check()
                mp.mp.dps = CFG['second_precision_digits']
                A2, _, _ = fixed_h_matrix(certificate_matrix(data), n)
                values2 = spectrum(A2)
                discrepancies = [abs(a-b)/abs(b) for a,b in zip(raw_values, values2)]
                row['second_precision'] = {'digits': mp.mp.dps,
                    'max_singular_relative_discrepancy': text_number(max(discrepancies)),
                    'smallest': text_number(values2[-1])}
                assert max(discrepancies) < mp.mpf('1e-35')
                mp.mp.dps = CFG['precision_digits']
            assert model.serialize() == before
            row['cpu_seconds'] = time.process_time() - begin
            append_jsonl(ROOT/'spectra.jsonl', row)
            results.append(row)
            print(f'{case} n={n}: complete, CPU {row["cpu_seconds"]:.2f}s; raw counts {row["fixed_h_raw"]["absolute_counts"]}', flush=True)
    assert {k: hashlib.sha256((REPO/k).read_bytes()).hexdigest() for k in hashes} == hashes
    (ROOT/'source_hashes.json').write_text(json.dumps(hashes, indent=2))
    (ROOT/'hardware.json').write_text(json.dumps(hardware, indent=2))
    (ROOT/'summary.json').write_text(json.dumps(results, indent=2))
    return results

if __name__ == '__main__':
    meter = Meter('archived spectra, fixed-h conditioning, independent controls and conservative patch radii')
    try:
        assert not (ROOT/'spectra.jsonl').exists(), 'Append-only: use a documented new output for any correction.'
        run(meter)
    finally:
        print(json.dumps(meter.finish()), flush=True)
