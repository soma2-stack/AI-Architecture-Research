"""CPU-only algebra checks, not a proof of asymptotic robust dimension.

One process; standard library; all numerical pools capped at one thread.
No CUDA imports, workers, full large-width simulation, or brute-force search.
"""
import os
for name in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS',
             'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
    os.environ[name] = '1'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

import ctypes
from ctypes import wintypes
from decimal import Decimal as D, getcontext
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math
import time

START = time.process_time()
RECORDS = []
PEAK_THREADS = 0
PEAK_RAM = 0

def resources():
    global PEAK_THREADS, PEAK_RAM
    if os.name != 'nt':
        return
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    psapi = ctypes.WinDLL('psapi', use_last_error=True)
    class ENTRY(ctypes.Structure):
        _fields_ = [('dwSize', wintypes.DWORD), ('cntUsage', wintypes.DWORD),
                    ('th32ThreadID', wintypes.DWORD), ('th32OwnerProcessID', wintypes.DWORD),
                    ('tpBasePri', wintypes.LONG), ('tpDeltaPri', wintypes.LONG),
                    ('dwFlags', wintypes.DWORD)]
    class PMC(ctypes.Structure):
        _fields_ = [('cb', wintypes.DWORD), ('PageFaultCount', wintypes.DWORD)] + [
            (name, ctypes.c_size_t) for name in ('PeakWorkingSetSize', 'WorkingSetSize',
            'QuotaPeakPagedPoolUsage', 'QuotaPagedPoolUsage', 'QuotaPeakNonPagedPoolUsage',
            'QuotaNonPagedPoolUsage', 'PagefileUsage', 'PeakPagefileUsage')]
    kernel.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    kernel.Thread32First.argtypes = [wintypes.HANDLE, ctypes.POINTER(ENTRY)]
    kernel.Thread32Next.argtypes = [wintypes.HANDLE, ctypes.POINTER(ENTRY)]
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    psapi.GetProcessMemoryInfo.argtypes = [wintypes.HANDLE, ctypes.POINTER(PMC), wintypes.DWORD]
    snap = kernel.CreateToolhelp32Snapshot(4, 0)
    if snap == ctypes.c_void_p(-1).value:
        raise RuntimeError('Thread inventory failed')
    entry = ENTRY()
    entry.dwSize = ctypes.sizeof(entry)
    count = 0
    valid = kernel.Thread32First(snap, ctypes.byref(entry))
    while valid:
        count += entry.th32OwnerProcessID == os.getpid()
        valid = kernel.Thread32Next(snap, ctypes.byref(entry))
    kernel.CloseHandle(snap)
    mem = PMC()
    mem.cb = ctypes.sizeof(mem)
    if not psapi.GetProcessMemoryInfo(kernel.GetCurrentProcess(), ctypes.byref(mem), mem.cb):
        raise RuntimeError('RAM inventory failed')
    PEAK_THREADS = max(PEAK_THREADS, count)
    PEAK_RAM = max(PEAK_RAM, mem.PeakWorkingSetSize)
    if count > 8 or PEAK_RAM > 128*1024**2:
        raise RuntimeError('Resource guard exceeded; do not increase budget')

def check(name, condition):
    if not condition:
        raise AssertionError(name)
    RECORDS.append({'check': name, 'status': 'PASS'})

def dot(x, y):
    return sum(u*v for u,v in zip(x,y))

def mv(a, x):
    return [dot(row,x) for row in a]

def mm(a,b):
    return [[dot(row,col) for col in zip(*b)] for row in a]

P = [[F(i==j)-F(1,5) for j in range(5)] for i in range(5)]
rates = [1,3,1,2,3]
R = mm(P, [[F(rates[i])*P[i][j] for j in range(5)] for i in range(5)])
w = [F(1),F(1),F(-1),F(-1),F(0)]
qr = [[F(0),F(0),F(-1),F(0),F(1)], [F(0),F(0),F(1),F(-2),F(1)]]

# Jacobian coefficients indexed by eta power. All calculations exact.
coef = [[[F(0)]*4 for _ in range(2)] for _ in range(2)]
for k in range(2):
    dk = [[P[i][k]*P[k][j] for j in range(5)] for i in range(5)]
    power = w[:]
    deriv = [F(0)]*5
    for order in range(1,5):
        deriv = [a+b for a,b in zip(mv(R,deriv),mv(dk,power))]
        power = mv(R,power)
        for row in range(2):
            coef[row][k][order-1] = F((-1)**order, math.factorial(order+1))*dot(qr[row],deriv)
expected = [
    [[F(0),F(-1,15),F(19,300),F(-49,1500)],
     [F(0),F(-1,15),F(13,100),F(-41,300)]],
    [[F(0),F(0),F(1,60),F(-29,1500)],
     [F(0),F(0),F(1,60),F(-49,1500)]]]
check('all fourth-order Jacobian coefficients exact', coef == expected)

def determinant_poly(coeff):
    out = [F(0)]*7
    for i in range(4):
        for j in range(4):
            out[i+j] += coeff[0][0][i]*coeff[1][1][j]-coeff[0][1][i]*coeff[1][0][j]
    return out

det = determinant_poly(coef)
check('determinant leading power is eta^4', det[:4] == [0]*4 and det[4] == F(-1,4500))
eta = F(1,10**6)
check('remaining determinant polynomial below 2 eta^5', sum(abs(det[j])*eta**j for j in (5,6)) < 2*eta**5)
check('strict determinant lower', eta**4/F(4500)-14*eta**5-36*eta**8 > eta**4/F(9000))
check('normalization loss below 100000', 18000**2*12 < 100000**2)
resources()

# Full Householder replay at n=512: identity only, outside theorem range.
n,k,r,d = 512,256,255,128
a = F(n-1,n)
gamma = F(16,15)
c = F(1,225)
u = [-c]*r
u[d-2] += gamma/16
vh = [gamma/16]*r
def op(x):
    out = [F(0)]*r
    for j in range(1,d-1):
        out[j] = x[j-1]
    for j in range(d-1,r):
        out[j] = x[j]
    j,b = dot(u,x),dot(vh,x)
    out = [q+j for q in out]
    out[0] += b
    return out

def sites(cohort,t):
    return [24+cohort+t,65+cohort+t,d+2*cohort,d+2*cohort+1]

v = [F(0)]*r
for cohort in range(4):
    for idx in sites(cohort,0)[2:]:
        v[idx] = w[cohort]
check('full replay fixed zero-sum probe stationary', op(v)==v and sum(v)==0)
x = [F(0)]*r
z = [F(0)]*5
lam = [eta*j for j in rates]
Wsmall = 4
for t in range(1,Wsmall+1):
    active = [idx for j in range(5) for idx in sites(j,t-1)]
    avg = sum(x[idx] for idx in active)/20
    q = x[:]
    for idx in active:
        q[idx] = avg
    oq = op(q)
    g = [F(999,1000)]*r
    for front in range(4):
        g[front] = F(front+1,n)
    for cohort in range(5):
        for idx in sites(cohort,t):
            g[idx] = 1-lam[cohort]/Wsmall
    ox = op(x)
    xnew = [g[idx]*(a*ox[idx]+v[idx]) for idx in range(r)]
    means = [sum(xnew[idx] for idx in sites(j,t))/2 for j in range(5)]
    znew = mv(P,means)
    e = mv(P, [sum(-a*lam[j]/Wsmall*oq[idx] for idx in sites(j,t))/2 for j in range(5)])
    pred = [a*z[j]+w[j]+e[j] for j in range(5)]
    correction = mv(P,[lam[j]*(a*z[j]+w[j])/Wsmall for j in range(5)])
    pred = [x-y for x,y in zip(pred,correction)]
    check(f'complete projected recurrence step {t}', pred==znew)
    x,z = xnew,znew
resources()

# Finite-difference geometry in Decimal precision, not a proof by sampling.
getcontext().prec = 100
def decimal(x):
    return D(x.numerator)/D(x.denominator)
Pd = [[decimal(x) for x in row] for row in P]
wd = [decimal(x) for x in w]
Qd = [[decimal(x)/D(2 if j==0 else 6).sqrt() for x in row] for j,row in enumerate(qr)]
fd = [x/(2*D(2).sqrt()) for x in wd]
ed,dd = D('1e-6'),D('1e-30')
def continuum(theta):
    vals = [ed,3*ed,ed,2*ed,3*ed]
    vals[0] += dd*theta[0]
    vals[1] += dd*theta[1]
    mat = mm(Pd, [[vals[i]*Pd[i][j] for j in range(5)] for i in range(5)])
    power = fd[:]
    out = power[:]
    for order in range(1,25):
        power = mv(mat,power)
        scale = D((-1)**order)/D(math.factorial(order+1))
        out = [x+scale*y for x,y in zip(out,power)]
    return mv(Qd,out)

j0 = [[sum(decimal(coef[i][j][p])*ed**p for p in range(4))/(2*D(2).sqrt()*D(2 if i==0 else 6).sqrt())
       for j in range(2)] for i in range(2)]
b = mm(list(map(list,zip(*j0))),j0)
trace = b[0][0]+b[1][1]
largest = (trace+((b[0][0]-b[1][1])**2+4*b[0][1]**2).sqrt())/2
smallest = (j0[0][0]*j0[1][1]-j0[0][1]*j0[1][0])**2/largest
weak = [b[0][1],smallest-b[0][0]]
directions = [[D(1),D(0)],[D(0),D(1)],[D(1),D(1)],[D(1),D(-1)],weak]
for q in range(24):
    angle = 2*math.pi*q/24
    directions.append([D(str(math.cos(angle))),D(str(math.sin(angle)))])
min_gain = None
for number,vec in enumerate(directions):
    size = sum(x*x for x in vec).sqrt()
    theta = [x/size for x in vec]
    plus,minus = continuum(theta),continuum([-x for x in theta])
    gain = sum(((x-y)/(2*dd))**2 for x,y in zip(plus,minus)).sqrt()
    min_gain = gain if min_gain is None else min(min_gain,gain)
    check(f'100-digit finite antipode {number}',gain>D('1e-23'))
resources()
root = Path(__file__).resolve().parent
result = {
    'meaning':'Algebra and small finite samples only; proof is in PROOF.md.',
    'passed':len(RECORDS),'checks':RECORDS,
    'exact_raw_jacobian_coefficients':[[[str(x) for x in col] for col in row] for row in coef],
    'exact_determinant_polynomial':[str(x) for x in det],
    'sampled_minimum_continuum_gain':str(min_gain),
    'decimal_precision':100,'full_replay_width':512,'full_replay_steps':4,
    'cpu_seconds':time.process_time()-START,'peak_observed_process_threads':PEAK_THREADS,
    'peak_working_set_bytes':PEAK_RAM,'arithmetic_pool_threads':1,'workers':0,
    'GPU_CUDA_usage':0,'checks_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'environment':{name:os.environ[name] for name in ('OMP_NUM_THREADS','MKL_NUM_THREADS',
                'OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS','CUDA_VISIBLE_DEVICES')}
}
(root/'checks_result.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:result[k] for k in ('passed','sampled_minimum_continuum_gain',
      'cpu_seconds','peak_observed_process_threads','peak_working_set_bytes','GPU_CUDA_usage')},indent=2))
