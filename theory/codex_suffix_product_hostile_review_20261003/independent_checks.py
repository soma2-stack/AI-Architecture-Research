"""Independent attacks on a static quantile obstruction; no original imports."""
import os
POOL_KEYS = ('OMP_NUM_THREADS', 'OMP_THREAD_LIMIT', 'MKL_NUM_THREADS',
             'OPENBLAS_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS',
             'VECLIB_MAXIMUM_THREADS', 'TBB_NUM_THREADS')
for key in POOL_KEYS:
    os.environ[key] = '1'
os.environ['OMP_DYNAMIC'] = 'FALSE'
os.environ['MKL_DYNAMIC'] = 'FALSE'
os.environ['OMP_MAX_ACTIVE_LEVELS'] = '1'
os.environ['CUDA_VISIBLE_DEVICES'] = ''
os.environ['NVIDIA_VISIBLE_DEVICES'] = 'void'

from pathlib import Path
from fractions import Fraction
import hashlib
import itertools
import json
import math
import time
import mpmath as mp
import numpy as np
import psutil

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROCESS = psutil.Process()
START = time.perf_counter()
CPU_START = sum(PROCESS.cpu_times()[:2])
CHECKS = []
PEAK_THREADS = 0
PEAK_RSS = 0


def guard():
    global PEAK_THREADS, PEAK_RSS
    PEAK_THREADS = max(PEAK_THREADS, PROCESS.num_threads())
    PEAK_RSS = max(PEAK_RSS, PROCESS.memory_info().rss)
    if PEAK_THREADS > 8 or PEAK_RSS > 192 * 1024**2 or PROCESS.children():
        raise RuntimeError('Resource policy exceeded: stop without more resources')


def record(name, condition, **data):
    guard()
    CHECKS.append(dict(name=name, passed=bool(condition), data=data))
    if not condition:
        raise AssertionError(name)


def product_row(gates, a):
    # Explicit products, rather than cumsum/log from the original implementation.
    return [a**(len(gates)-j-1) * mp.fprod(gates[j:])
            for j in range(len(gates))]


def inverse_level(row, level):
    values = [mp.mpf(0)] + list(row) + [mp.mpf(1)]
    for j in range(len(values)-1):
        if values[j] <= level <= values[j+1]:
            return j + (level-values[j])/(values[j+1]-values[j])
    raise ValueError('Level outside the public anchors')


def code(row, p):
    return [inverse_level(row, mp.mpf(j)/p) for j in range(1, p)]


def reconstruct(row, p):
    knots = [mp.mpf(0)] + code(row, p) + [mp.mpf(len(row)+1)]
    result = []
    for x in range(1, len(row)+1):
        j = next(j for j in range(p) if knots[j] <= x <= knots[j+1])
        result.append((j + (x-knots[j])/(knots[j+1]-knots[j]))/p)
    return result


def integer_p(n, m, t):
    # Ceil sqrt(R) is computed exactly before dividing by the integer n.
    radicand = 16000**2*m*t*min(m,t)
    low = math.isqrt(radicand)
    root_ceiling = low + (low*low != radicand)
    return max(1, (root_ceiling+n-1)//n)


def flat_and_knot_attacks():
    answers = []
    for bits in (256, 384):
        with mp.workprec(bits):
            e = mp.mpf('1e-30')
            left = [mp.mpf('.5')-2*e, mp.mpf('.5')-e]
            right = [mp.mpf('.5')+e, mp.mpf('.5')+2*e]
            lpos = inverse_level(left, mp.mpf('.5'))
            rpos = inverse_level(right, mp.mpf('.5'))
            record(f'flat_extension_fails_{bits}',
                   abs(lpos-2)<4*e and abs(rpos-1)<4*e,
                   left_limit=mp.nstr(lpos, 55), right_limit=mp.nstr(rpos, 55),
                   scope='Flat limit is NOT a legal suffix-product row')
            # Near-flat reachable row, including a level chosen at a knot.
            a = 1-mp.mpf(1)/10**30
            g = mp.mpf(1)-mp.mpf('1e-32')
            base = product_row([g]*4, a)
            target = base[1]
            changes = []
            for step in ('1e-35', '1e-38', '1e-41'):
                h = mp.mpf(step)
                positions = [inverse_level(product_row([g+s*h]*4, a), target)
                             for s in (-1, 1)]
                changes.append(max(abs(x-2) for x in positions))
            record(f'legal_near_flat_continuity_{bits}',
                   changes[0]>changes[1]>changes[2] and changes[2]<mp.mpf('1e-9'),
                   position_changes=[mp.nstr(x,35) for x in changes])
            # Exact quantile .5 at a knot of an admissible T=200 row.
            n = 10**6
            a = 1-mp.mpf(1)/n
            t = 200
            node = 61
            length = t-node+1
            g = (mp.mpf('.5')/a**(length-1))**(mp.mpf(1)/length)
            base = product_row([g]*t, a)
            original = inverse_level(base, mp.mpf('.5'))
            positions = []
            err = 0
            for s in (-1, 0, 1):
                row = product_row([g+s*mp.mpf('1e-20')]*t, a)
                positions.append(inverse_level(row, mp.mpf('.5')))
                err = max(err, max(abs(x-y) for x,y in zip(row,reconstruct(row,4))))
            record(f'exact_knot_crossing_{bits}',
                   mp.mpf('.99')<g<1 and abs(original-node)<mp.mpf('1e-65')
                   and max(abs(x-node) for x in positions)<mp.mpf('1e-12') and err<=mp.mpf('.25'),
                   gate=mp.nstr(g,50), positions=[mp.nstr(x,55) for x in positions],
                   maximum_entry_error=mp.nstr(err,45))
            answers.append(mp.nstr(g,45))
    record('256_384_knot_gate_agreement', answers[0]==answers[1])


def equal_code_attacks():
    with mp.workprec(256):
        n = 10**6
        a = 1-mp.mpf(1)/n
        for m,t in ((2,30),(30,2),(8,8),(6,19),(19,6),(64,16),(16,64),(64,64)):
            p = integer_p(n,m,t)
            # Pick g so all internal levels fall in the first interpolation
            # segment. Move equal-and-opposite log mass between first/last gates.
            g = mp.mpf('.99999')
            ratio = mp.mpf(1)+mp.mpf('0.000003')
            plus = [g]*t
            minus = [g]*t
            plus[0],plus[-1] = g*ratio,g/ratio
            minus[0],minus[-1] = g/ratio,g*ratio
            x = product_row(plus,a)
            y = product_row(minus,a)
            cx,cy = code(x,p),code(y,p)
            difference = np.zeros((m,m+t-1))
            for i in range(m):
                difference[i,i:i+t] = [float(v-w) for v,w in zip(x,y)]
            # All nonzero errors have the SAME sign, so the all-ones sign
            # vector realizes the exact infinity-to-2 supremum.
            worst = float(np.linalg.norm(np.sum(difference,axis=0)))
            if m<=8:
                enumerated = max(float(np.linalg.norm(np.asarray(signs)@difference))
                                 for signs in itertools.product((-1,1),repeat=m))
            else:
                enumerated = worst
            upper = 8*worst/n + 8e-9
            bound = math.sqrt(m*t*min(m,t))
            decoded_error = max(abs(v-w) for v,w in zip(x,reconstruct(x,p)))
            record(f'equal_code_aligned_m{m}_T{t}_p{p}',
                   min(x+y)>1-mp.mpf(1)/p
                   and max([abs(v-w) for v,w in zip(cx,cy)]+[mp.mpf(0)])<mp.mpf('1e-65')
                   and decoded_error<=mp.mpf(1)/p
                   and abs(worst-enumerated)<1e-14
                   and worst<=2*bound/p and upper<.002,
                   p=p, code_coordinates=m*(p-1), exact_sign_norm=worst,
                   full_query_controlled_upper=upper,
                   max_entry_difference=mp.nstr(max(abs(v-w) for v,w in zip(x,y)),40))
        for m,t in ((2,25),(25,2),(7,7),(3,14),(14,3)):
            # Errors aligned in ONE column make the support factor sharp.
            E = np.zeros((m,m+t-1))
            counts = [sum(i<=j<i+t for i in range(m)) for j in range(m+t-1)]
            column = counts.index(max(counts))
            for i in range(m):
                if i<=column<i+t:
                    E[i,column] = 1
            H = float(np.linalg.norm(np.sum(E,axis=0)))
            F = float(np.linalg.norm(E))
            record(f'sharp_support_m{m}_T{t}',
                   max(counts)==min(m,t) and abs(H-math.sqrt(min(m,t))*F)<1e-12,
                   column_overlap=max(counts), H=H, frobenius=F)


def p_and_geometry():
    with mp.workprec(256):
        for n,m,t in ((10**6,1,1),(10**6,100,1000),(10**6,1000,100),
                      (10**12,10**8,10**5),(10**24,10**21,10**9),
                      (10**24,10**9,10**21),(16000,1,1)):
            p = integer_p(n,m,t)
            P = m*t
            s = min(m,t)
            Q = 16000*mp.sqrt(P*s)/n
            k = m*(p-1)
            record(f'integer_count_{n}_{m}_{t}',
                   p>=Q and p-1<Q and k<16000*mp.mpf(P)/mp.sqrt(n)
                   and 16*mp.sqrt(P*s)/(n*p)<=mp.mpf('.001'),
                   p=p, code_count=k, Q=mp.nstr(Q,30),
                   note='Last test is an arithmetic equality case, outside model n range')
        for t in (2,5,11,29):
            a = 1-mp.mpf(1)/10**6
            gates = [mp.mpf('.991')+mp.mpf('.0002')*(i%7) for i in range(t)]
            k = product_row(gates,a)
            inverse = [k[j]/(a*k[j+1]) for j in range(t-1)]+[k[-1]]
            diagonal = mp.fprod(k[j]/gates[j] for j in range(t))
            determinant = a**(t*(t-1)//2)*mp.fprod(gates[s]**s for s in range(1,t))
            record(f'product_inverse_determinant_T{t}',
                   max(abs(x-y) for x,y in zip(gates,inverse))<mp.mpf('1e-65')
                   and abs(diagonal-determinant)<mp.mpf('1e-65') and diagonal>0)
        q = 1/mp.cosh(mp.mpf('.25'))**2
        envelope = 1+6/(mp.mpf('.06')*mp.e)
        e = mp.mpf(4)/(10**8*mp.mpf(10**6)**2)
        sigma = mp.findroot(lambda s:s-mp.tanh(s/(100*10**6)+mp.mpf('.05')),mp.mpf('.05'))
        old = e*sigma*mp.sqrt(10**6)*10**6
        future = e*sigma*mp.sqrt(10**6)/(mp.mpf('.06')*mp.e)
        record('all_future_and_dense_constants', q<mp.e**(-mp.mpf('.06'))
               and envelope<100 and 100*mp.sqrt(2)*mp.mpf('.051')<8
               and old+future<mp.mpf('4e-9')
               and q**125000<mp.mpf('.001'),
               q=mp.nstr(q,50), all_horizon_envelope=mp.nstr(envelope,40),
               coefficient_cap=mp.nstr(100*mp.sqrt(2)*mp.mpf('.051'),40),
               past_dense_upper=mp.nstr(old,35), future_dense_upper=mp.nstr(future,35))


def independent_future_transport():
    # Only vector operations; no dense n-by-n matrix or GPU call.
    n = 10**6
    k = n//2
    d = n//4
    w = np.full(k,-1/math.sqrt(k))
    w[0] += 1
    gamma = 1/(1-1/math.sqrt(k))
    def U(v):
        return v-gamma*w*np.dot(w,v)
    def O(v):
        h = U(v)
        shifted = h.copy()
        shifted[0] = h[d-1]
        shifted[1:d] = h[:d-1]
        return U(shifted)
    column = 45
    unit = np.zeros(k)
    unit[column] = 1
    target = np.zeros(k)
    target[column+1] = 1
    leakage = float(np.linalg.norm(O(unit)-target))
    record('ordinary_cycle_column_leakage', leakage<6/math.sqrt(n),
           actual_leakage=leakage, allowed=6/math.sqrt(n))
    hi = 1/math.cosh(.25)**2
    lo = 1/math.cosh(.75)**2
    results = []
    for strategy in ('uniform_high','greedy_positive','greedy_negative'):
        v = np.zeros(k)
        v[column] = 1/math.sqrt(2)
        v[column+54] = -1/math.sqrt(2)
        for L in range(1,65):
            guard()
            moved = (1-1/n)*O(v)
            if strategy=='uniform_high':
                v = hi*moved
            elif strategy=='greedy_positive':
                v = np.where(moved>=0,hi,lo)*moved
            else:
                v = np.where(moved<=0,hi,lo)*moved
            if L in (1,2,8,16,32,64):
                # head dot forward propagated pair equals effective paired adjoint.
                scaled = abs(float(np.sum(v)))
                cap = math.sqrt(2)*hi**L*(1+6*L)
                record(f'multistep_query_{strategy}_L{L}', scaled<=cap+1e-12,
                       sqrt_n_times_pair_adjoint=scaled, analytic_envelope=cap)
                results.append(scaled)
    record('all_sampled_pair_components_below_uniform_100sqrt2',max(results)<100*math.sqrt(2),
           maximum_sqrt_n_times_pair_adjoint=max(results),
           limitation='Greedy legal words are attacks, not an optimization of every possible word')


outcome = 'PASS'
try:
    guard()
    flat_and_knot_attacks()
    equal_code_attacks()
    p_and_geometry()
    independent_future_transport()
except Exception as exc:
    outcome = 'FAIL'
    CHECKS.append(dict(name='first_failure',passed=False,data=dict(error=repr(exc))))
guard()
report = dict(outcome=outcome, checks=CHECKS,
              pool_settings={key:os.environ[key] for key in POOL_KEYS},
              cuda_visible_devices=os.environ['CUDA_VISIBLE_DEVICES'],
              gpu_usage=0, child_processes=0, peak_threads=PEAK_THREADS,
              peak_rss_bytes=PEAK_RSS,
              peak_working_set_bytes=getattr(PROCESS.memory_info(),'peak_wset',PEAK_RSS),
              cpu_seconds=sum(PROCESS.cpu_times()[:2])-CPU_START,
              wall_seconds=time.perf_counter()-START,
              precision_bits=[256,384],
              script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              status='NUMERICAL ATTACKS; analytic derivation supplies uniform theorem')
target = HERE/'independent_results.json'
if target.exists():
    raise RuntimeError('Preserve prior evidence; refusing to overwrite')
target.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({key:report[key] for key in ('outcome','cpu_seconds','wall_seconds',
                                           'peak_threads','peak_working_set_bytes')}))
raise SystemExit(0 if outcome=='PASS' else 1)
