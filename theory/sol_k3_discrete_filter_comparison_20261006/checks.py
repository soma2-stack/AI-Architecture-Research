"""Independent K=3 exact certificates. No source checks imported or run.

Standard library only, one process/pool, no workers or GPU APIs.
The rational proof is in PROOF.md; numerical eigenvalues are illustrative.
"""
import os
for name in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS',
             'NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[name]='1'
os.environ['CUDA_VISIBLE_DEVICES']='-1'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
import ctypes
from ctypes import wintypes
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math
import time

START=time.process_time()
RECORDS=[]
PEAK_THREADS=0
PEAK_RAM=0
def resources():
    global PEAK_THREADS,PEAK_RAM
    if os.name!='nt':
        return
    kernel=ctypes.WinDLL('kernel32',use_last_error=True)
    psapi=ctypes.WinDLL('psapi',use_last_error=True)
    class ENTRY(ctypes.Structure):
        _fields_=[('dwSize',wintypes.DWORD),('cntUsage',wintypes.DWORD),
                  ('th32ThreadID',wintypes.DWORD),('th32OwnerProcessID',wintypes.DWORD),
                  ('tpBasePri',wintypes.LONG),('tpDeltaPri',wintypes.LONG),('dwFlags',wintypes.DWORD)]
    class PMC(ctypes.Structure):
        _fields_=[('cb',wintypes.DWORD),('PageFaultCount',wintypes.DWORD)]+[
            (name,ctypes.c_size_t)for name in ('PeakWorkingSetSize','WorkingSetSize',
            'QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage','QuotaPeakNonPagedPoolUsage',
            'QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage')]
    kernel.CreateToolhelp32Snapshot.restype=wintypes.HANDLE
    kernel.Thread32First.argtypes=[wintypes.HANDLE,ctypes.POINTER(ENTRY)]
    kernel.Thread32Next.argtypes=[wintypes.HANDLE,ctypes.POINTER(ENTRY)]
    kernel.CloseHandle.argtypes=[wintypes.HANDLE]
    kernel.GetCurrentProcess.restype=wintypes.HANDLE
    psapi.GetProcessMemoryInfo.argtypes=[wintypes.HANDLE,ctypes.POINTER(PMC),wintypes.DWORD]
    snap=kernel.CreateToolhelp32Snapshot(4,0)
    if snap==ctypes.c_void_p(-1).value:
        raise RuntimeError('Thread inventory failed')
    entry=ENTRY();entry.dwSize=ctypes.sizeof(entry)
    count=0;valid=kernel.Thread32First(snap,ctypes.byref(entry))
    while valid:
        count+=entry.th32OwnerProcessID==os.getpid()
        valid=kernel.Thread32Next(snap,ctypes.byref(entry))
    kernel.CloseHandle(snap)
    mem=PMC();mem.cb=ctypes.sizeof(mem)
    if not psapi.GetProcessMemoryInfo(kernel.GetCurrentProcess(),ctypes.byref(mem),mem.cb):
        raise RuntimeError('RAM inventory failed')
    PEAK_THREADS=max(PEAK_THREADS,count)
    PEAK_RAM=max(PEAK_RAM,mem.PeakWorkingSetSize)
    if count>8 or PEAK_RAM>128*1024**2:
        raise RuntimeError('Resource guard exceeded; stop, do not increase budget')

def check(name,condition):
    if not condition:
        raise AssertionError(name)
    RECORDS.append({'check':name,'status':'PASS'})
def mm(a,b):
    return [[sum(a[i][k]*b[k][j]for k in range(len(b)))for j in range(len(b[0]))]for i in range(len(a))]
def det(a):
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
            -a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
            +a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))
def minors(a):
    return [a[0][0],a[0][0]*a[1][1]-a[0][1]*a[1][0],det(a)]
def shift(a,x):
    return [[a[i][j]-x*F(i==j)for j in range(3)]for i in range(3)]
resources()

# Derive the three Paley words on exactly four panels.
words=[]
for index in (1,2,3):
    signs=[]
    for panel in range(4):
        midpoint=F(2*panel+1,8); value=1
        for bit in (0,1):
            if (index&(1<<bit)) and ((midpoint*(1<<bit))%1>=F(1,2)):
                value=-value
        signs.append(value)
    words.append(signs)
check('exact three Paley words',words==[[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]])
polys=[]
for signs in words:
    acc=F(0); row=[]
    for panel,sign in enumerate(signs):
        left,right=F(panel,4),F(panel+1,4)
        row.append([acc-sign*left*left/2,F(sign,2)])
        acc+=sign*(right*right-left*left)/2
    polys.append(row)
G=[[F(0)]*3 for _ in range(3)]
for i in range(3):
    for j in range(3):
        for panel in range(4):
            left,right=F(panel,4),F(panel+1,4)
            x,y=polys[i][panel],polys[j][panel]
            G[i][j]+=(x[0]*y[0]*(right-left)
                      +(x[0]*y[1]+x[1]*y[0])*(right**3-left**3)/3
                      +x[1]*y[1]*(right**5-left**5)/5)
expected=[[F(x,7680)for x in row]for row in [[64,5,10],[5,14,-10],[10,-10,74]]]
check('exact independently integrated Gram',G==expected)
for i,x in enumerate(minors(G)):
    check(f'Gram positive minor {i}',x>0)
low,high=F(3876,100000),F(3878,100000)
for i,x in enumerate(minors(shift(G,low**2))):
    check(f'lower eigenvalue certificate {i}',x>0)
check('upper eigenvalue certificate',det(shift(G,high**2))<0)
check('trace bound',sum(G[i][i]for i in range(3))==F(19,960)<F(1,40))
Q=[[F(1,2),F(-1,2),F(1,2),F(-1,2)],
   [F(1,2),F(1,2),F(-1,2),F(-1,2)],
   [F(1,2),F(-1,2),F(-1,2),F(1,2)]]
check('specified survivor basis orthonormal',mm(Q,list(map(list,zip(*Q))))==[[F(i==j)for j in range(3)]for i in range(3)])
check('first survivor column', [row[0]for row in Q]==[F(1,2)]*3)

# Independently verify the rational inverse-square-root certificate.
M=[[11190504,-1715279,-997092],[-1715279,25098676,2619403],[-997092,2619403,10598990]]
B=[[F(x,10**6)for x in row]for row in M]
check('certificate symmetric',B==list(map(list,zip(*B))))
for i,x in enumerate(minors(shift(B,F(8)))):
    check(f'certificate B>8I minor {i}',x>0)
adj=[[936,-470,-190],[-470,4636,690],[-190,690,871]]
inv=[[F(3840*x,27827)for x in row]for row in adj]
check('exact Gram inverse',mm(G,inv)==[[F(i==j)for j in range(3)]for i in range(3)])
square=mm(B,B)
R=[[square[i][j]-inv[i][j]for j in range(3)]for i in range(3)]
numerators=[[int(x*27827*10**12)for x in row]for row in R]
check('exact residual numerator matrix',numerators==[[-209697161533,492364924208,71643230105],
     [492364924208,-479294032098,-314840249418],[71643230105,-314840249418,-71781420329]])
for i in range(3):
    for j in range(3):
        check(f'exact residual entry bound {i},{j}',abs(R[i][j])<F(1,1000))
check('Sylvester certificate bound',F(1,100)/14==F(1,1400))
def Fvec(u):
    panel=min(int(u*4),3)
    return [polys[i][panel][0]+polys[i][panel][1]*u*u for i in range(3)]
def sumBF(vec):
    return sum(B[i][j]*vec[j]for i in range(3)for j in range(3))
s0=F(15,16)
value=sumBF(Fvec(s0))
check('exact final-interval start value',value==F(-128708227,32000000))
err=F(3,2800)
check('strict negative rate certificate',value+err < -F(201,50))
check('exact strict-gap value',-F(201,50)-(value+err)==F(237589,224000000))
slope=sumBF([F(-1,2),F(-1,2),F(1,2)])
check('exact negative final-panel slope',slope==F(-1391227,125000))
check('slope remains negative with inverse-root error',slope+err<0)
check('exact endpoint integrated codes',Fvec(F(1))==[F(-1,4),F(-1,8),F(0)])
check('stronger endpoint rate bound',sumBF(Fvec(F(1)))+err < -F(16,3))
for W in (16,17,31,32,101,10**810):
    first=(15*W+15)//16
    check(f'number of bad samples W bits={W.bit_length()}',W-first+1==W//16+1)
    check(f'strict illegal gate W bits={W.bit_length()}',1+F(1,10**6*200*W)>1)
resources()

# Small independent Jacobi calculation, illustrative only.
A=[[float(x)for x in row]for row in G]
V=[[float(i==j)for j in range(3)]for i in range(3)]
for _ in range(80):
    p,q=max(((i,j)for i in range(3)for j in range(i+1,3)),key=lambda ij:abs(A[ij[0]][ij[1]]))
    if abs(A[p][q])<1e-18:
        break
    angle=.5*math.atan2(2*A[p][q],A[q][q]-A[p][p])
    co,si=math.cos(angle),math.sin(angle)
    rot=[[float(i==j)for j in range(3)]for i in range(3)]
    rot[p][p]=rot[q][q]=co;rot[p][q]=si;rot[q][p]=-si
    A=mm(mm(list(map(list,zip(*rot))),A),rot);V=mm(V,rot)
eigs=[A[j][j]for j in range(3)]
Hnum=[[sum(V[i][k]*V[j][k]/math.sqrt(eigs[k])for k in range(3))for j in range(3)]for i in range(3)]
end=Fvec(F(1))
endpoint=1+.25*sum(Hnum[i][j]*float(end[j])for i in range(3)for j in range(3))
resources()
root=Path(__file__).resolve().parent
result={'scope':'K=3 literal matched bank only; exact countercertificate, not a dimension upper',
        'passed':len(RECORDS),'checks':RECORDS,
        'exact_Gram':[[str(x)for x in row]for row in G],
        'numerical_Gram_eigenvalues':sorted(eigs),
        'numerical_sigma_min_M3':math.sqrt(min(eigs)),
        'numerical_endpoint_first_survivor_rate_over_eta':endpoint,
        'exact_rate_upper_final_interval':'-eta/200',
        'exact_rate_upper_endpoint':'-eta/3',
        'cpu_seconds':time.process_time()-START,
        'peak_observed_process_threads':PEAK_THREADS,'peak_working_set_bytes':PEAK_RAM,
        'arithmetic_pool_threads':1,'workers':0,'GPU_CUDA_usage':0,
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'environment':{name:os.environ[name]for name in ('OMP_NUM_THREADS','MKL_NUM_THREADS',
                       'OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS','CUDA_VISIBLE_DEVICES')}}
(root/'checks_result.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({key:result[key]for key in ('passed','numerical_sigma_min_M3',
      'numerical_endpoint_first_survivor_rate_over_eta','cpu_seconds',
      'peak_observed_process_threads','peak_working_set_bytes','GPU_CUDA_usage')},indent=2))
