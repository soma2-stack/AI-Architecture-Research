"""Independent small CPU identities. Numerical results are not dimension proofs."""
import os
POOLS=('OMP_NUM_THREADS','OMP_THREAD_LIMIT','MKL_NUM_THREADS',
       'OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS',
       'VECLIB_MAXIMUM_THREADS','TBB_NUM_THREADS')
for name in POOLS:
    os.environ[name]='1'
os.environ['OMP_DYNAMIC']='FALSE'
os.environ['MKL_DYNAMIC']='FALSE'
os.environ['OMP_MAX_ACTIVE_LEVELS']='1'
os.environ['CUDA_VISIBLE_DEVICES']=''
os.environ['NVIDIA_VISIBLE_DEVICES']='void'
import hashlib
import itertools
import json
import math
import time
from pathlib import Path
import numpy as np
import mpmath as mp
import psutil

HERE=Path(__file__).resolve().parent
PROC=psutil.Process()
START=time.perf_counter(); CPU0=sum(PROC.cpu_times()[:2])
PEAK_THREADS=0; PEAK_RAM=0; RECORDS=[]
try:
    from threadpoolctl import threadpool_info
    LIBRARIES=threadpool_info()
except ImportError:
    LIBRARIES=[]

def guard():
    global PEAK_THREADS,PEAK_RAM
    PEAK_THREADS=max(PEAK_THREADS,PROC.num_threads())
    PEAK_RAM=max(PEAK_RAM,PROC.memory_info().rss)
    if PEAK_THREADS>8 or PEAK_RAM>160*1024**2 or PROC.children():
        raise RuntimeError('Resource stop; no increased-resource retry')

def save(status):
    guard()
    value=dict(status=status,checks=RECORDS,seed=20261003,
        cpu_seconds=sum(PROC.cpu_times()[:2])-CPU0,
        wall_seconds=time.perf_counter()-START,
        peak_observed_process_threads=PEAK_THREADS,
        peak_observed_working_set_bytes=PEAK_RAM,
        library_pools={key:os.environ[key] for key in POOLS},
        library_metadata=LIBRARIES,workers=0,gpu_cuda_calls=0,
        numpy_version=np.__version__,mpmath_version=mp.__version__,
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (HERE/'checks_result.json').write_text(json.dumps(value,indent=2)+'\n')

def check(name,ok,**data):
    guard(); RECORDS.append(dict(name=name,passed=bool(ok),data=data))
    if not ok:
        save('FAILED'); raise AssertionError(name)

class Model:
    def __init__(self,n):
        self.n=n; self.k=n//2; self.r=self.k-1; self.d=n//4
        self.a=1-1/n; self.gamma=1/(1-1/math.sqrt(self.k))
        self.c=self.gamma**2/self.k
        self.u=np.full(self.r,-self.c)
        self.u[self.d-2]+=self.gamma/math.sqrt(self.k)
        self.v=np.full(self.r,self.gamma/math.sqrt(self.k))
    def C(self,x):
        y=x.copy(); y[0]=0; y[1:self.d-1]=x[:self.d-2]
        return y
    def O(self,x):
        y=self.C(x)
        if x.ndim==1:
            y+=self.u@x; y[0]+=self.v@x
        else:
            y+=(self.u@x)[None,:]; y[0]+=self.v@x
        return y
    def sites(self,m,T,t):
        S=m+T+4
        # Array indices equal physical selected coordinates minus one.
        return np.array([[2*S+i+t,5*S+i+t,self.d+2*i+3,
                          self.d+2*i+4] for i in range(m)])

def prepare(z,m,T):
    h=np.full(z.r,math.tanh(.05)); sites=z.sites(m,T,0)
    h[sites]=[.04,.04,-.04,-.04]
    return h

def step(z,m,T,t,h,g):
    pre=z.a*z.O(h)+.05
    nxt=np.tanh(pre); sites=z.sites(m,T,t)
    # This ordinary row is before the corridor and beyond the front.
    bath=float(nxt[m+T+4])
    if t<=T:
        beta=np.sqrt(1-g)
        nxt[sites]=np.column_stack((beta,beta,-beta,-beta))
    else:
        nxt[sites]=bath
    x=np.arctanh(nxt[sites])-pre[sites]
    return nxt,1-nxt*nxt,bath,float(np.sum(x*x)),float(np.max(abs(x)))

def full_small():
    # n=512 is only an exact reference identity test, not an admitted
    # asymptotic theorem candidate or finite-error certificate.
    z=Model(512); m=2; T=5; I=np.eye(z.r)
    O=z.O(I); C=z.C(I)
    check('Ostar orthogonal small',np.max(abs(O.T@O-I))<3e-14)
    h=prepare(z,m,T); M=np.zeros_like(I); L=M.copy(); Lbar=M.copy()
    ellbar=[]; gates=[]; bank=[]
    U=set(z.sites(m,T,0)[:,2:].ravel().tolist())
    for t in range(1,T+2):
        ellbar.extend([z.u@Lbar,z.v@Lbar])
        g=np.array([.9945+.00004*t,.998])
        h,G,bath,_,_=step(z,m,T,t,h,g)
        gb=G.copy()
        if t<=T:
            gb[z.sites(m,T,t).ravel()]=1-bath*bath
            U.update(z.sites(m,T,t)[:,:2].ravel().tolist())
        M=G[:,None]*(z.a*z.O(M)+I)
        L=G[:,None]*(z.a*z.C(L)+I)
        Lbar=gb[:,None]*(z.a*z.C(Lbar)+I)
        gates.append(G); bank.append(M.copy())
        guard()
    U=sorted(U)
    outside=np.ones(z.r,dtype=bool); outside[U]=False
    check('direct private columns localized',np.max(abs((L-Lbar)[:,outside]))<2e-14)
    span=np.column_stack([I[:,U],np.array(ellbar).T])
    qbasis,sv,_=np.linalg.svd(span,full_matrices=False)
    rank=int(np.sum(sv>1e-11)); qbasis=qbasis[:,:rank]
    H=M-L
    residual=np.max(abs(H-(H@qbasis)@qbasis.T))
    check('all-orders private public right-subspace',residual<2e-12,
          residual=float(residual),numerical_span_rank=rank,upper=4*m+4*T+2)
    # Epoch boundaries 2,4,6; separately form affine epoch maps.
    composed=np.zeros_like(I)
    left=0
    for right in (2,4,T+1):
        ae=I.copy(); be=np.zeros_like(I)
        for G in gates[left:right]:
            at=z.a*G[:,None]*O
            ae=at@ae; be=at@be+G[:,None]*I
        composed=ae@composed+be; left=right
    check('exact multi-epoch affine composition',np.max(abs(composed-M))<3e-13)
    sites=z.sites(m,T,T+1)
    for i in range(m):
        v=I[:,sites[i,2]]-I[:,sites[i,3]]
        check(f'twin compensator private annihilator {i}',np.linalg.norm(H@v)<2e-13)
    far1=z.d+2*m+10; far2=far1+1
    check('ordinary offcycle private annihilator',np.linalg.norm(H@(I[:,far1]-I[:,far2]))<2e-13)
    # Pure cohort read-frame audit. Not a lower bound on the generated
    # transfer matrix; no ambient matrix is called reachable.
    W=np.zeros((z.r,m)); Wnext=W.copy()
    for i in range(m):
        W[sites[i],i]=.5; Wnext[z.sites(m,T,T+2)[i],i]=.5
    B=Wnext.T@O@W
    expected=np.eye(m)-4*z.c*np.ones((m,m))
    check('exact cohort query overlap',np.max(abs(B-expected))<2e-14,
          eigenvalues=np.linalg.eigvalsh(B).tolist())
    rng=np.random.default_rng(20261003); X=rng.normal(size=(m,7))
    A=W@X; hi=1/math.cosh(.25)**2; lo=1/math.cosh(.75)**2
    center=(hi+lo)/2; sg=(hi-lo)/2
    witness=0.; maximum_query=0.
    for signs in itertools.product((-1,1),repeat=m):
        signed=Wnext@(2*np.array(signs))
        witness=max(witness,np.linalg.norm(X.T@B@(2*np.array(signs))))
        for polarity in (-1,1):
            gq=np.full(z.r,center)+polarity*sg*signed
            maximum_query=max(maximum_query,np.linalg.norm(A.T@O.T@gq))
    check('legal complementary sign witness lower',maximum_query+1e-13>=sg*witness)
    fro_bound=2*(1-8*z.c)*np.linalg.norm(X)
    check('Rademacher witness is legal supremum lower',witness+1e-13>=fro_bound,
          witness=float(witness),fro_lower=float(fro_bound))

def word(z,m,T,tail,theta,derivative=False,change_survivor=False):
    donors=3; t0=T-tail; g=np.empty((m,T)); dg=np.zeros_like(g)
    for i in range(donors):
        for t in range(t0):
            epoch=min(2,3*t//t0)
            coefficient=(i+1)*(epoch+1)/9
            coordinate=theta if np.ndim(theta)==0 else theta[i,epoch]
            g[i,t]=.995+1e-5*coefficient*coordinate
            differentiated=(not isinstance(derivative,tuple)) or derivative==(i,epoch)
            dg[i,t]=1e-5*coefficient if differentiated else 0.
        g[i,t0:T-1]=.995
        state=dst=base=0.
        for t in range(T-1):
            dst=dg[i,t]*(1+z.a*state)+z.a*g[i,t]*dst
            state=g[i,t]*(1+z.a*state)
            base=.995*(1+z.a*base)
        target=.995*(1+z.a*base)
        g[i,-1]=target/(1+z.a*state)
        dg[i,-1]=-target*z.a*dst/(1+z.a*state)**2
    for i in range(donors,m):
        g[i]=.997+1e-6*np.sin(np.arange(T)/3)
        if i==m-1 or (change_survivor and i==donors+1):
            g[i,:T//2]-=1e-5
    return g,dg

def stream(theta,derivative=False,change_survivor=False):
    z=Model(65536); m=6; T=32; tail=8
    sites=z.sites(m,T,0)
    # Orthonormal input probes: six compensator pair sums, one twin
    # difference, one ordinary offcycle difference, three cycle coordinates.
    P=np.zeros((z.r,m+5))
    for i in range(m): P[sites[i,2:],i]=1/math.sqrt(2)
    P[sites[0,2:],m]=[1/math.sqrt(2),-1/math.sqrt(2)]
    P[z.d+2*m+20,m+1]=1/math.sqrt(2)
    P[z.d+2*m+21,m+1]=-1/math.sqrt(2)
    for j in range(3): P[z.sites(m,T,1+j)[0,0],m+2+j]=1
    g,dg=word(z,m,T,tail,theta,derivative,change_survivor)
    h=prepare(z,m,T); X=np.zeros_like(P); L=X.copy(); dX=X.copy()
    V=np.zeros((m,P.shape[1])); Z=np.zeros(P.shape[1]); traces=np.zeros(m)
    energy=float(np.sum((np.arctanh(h[sites])-.05)**2))
    maxrow=0.; maxword=0.; maxinput=0.; maxfront=0.
    q=.9992
    for t in range(1,T+2):
        J=z.u@X
        h,G,bath,ecost,inputmax=step(z,m,T,t,h,g[:,min(t-1,T-1)])
        energy+=ecost; maxinput=max(maxinput,inputmax)
        ss=z.sites(m,T,t)
        dG=np.zeros(z.r)
        if t<=T:
            dG[ss]=dg[:,t-1,None]
            traces=g[:,t-1]*(1+z.a*traces)
        if derivative:
            dX=dG[:,None]*(z.a*z.O(X)+P)+G[:,None]*z.a*z.O(dX)
        X=G[:,None]*(z.a*z.O(X)+P)
        L=G[:,None]*(z.a*z.C(L)+P)
        V=z.a*G[ss[:,0],None]*(V+J)
        Z=z.a*(1-bath*bath)*(Z+J)
        H=X-L
        maxrow=max(maxrow,float(np.max(abs(H[ss]-V[:,None,:]))))
        maxword=max(maxword,float(np.max(abs(V[3]-V[4]))))
        front=H[:t]-Z
        constant=8000*(T+1)/math.sqrt(z.n)
        front_upper=constant*np.arange(1,t+1)*q**np.arange(t)
        maxfront=max(maxfront,float(np.max(np.linalg.norm(front,axis=1)/front_upper)))
        guard()
    sigma=.05
    for _ in range(20): sigma=math.tanh(.05+sigma/(100*z.n))
    energy+=(z.n-z.k)*(sigma/(100*z.n))**2
    result=dict(X=X,L=L,H=X-L,dX=dX,h=h,V=V,Z=Z,traces=traces,
        energy=energy,maxinput=maxinput,maxrow=maxrow,maxword=maxword,
        maxfront=maxfront,gates=g,sites=z.sites(m,T,T+1),model=z,probes=P)
    return result

def stream_checks():
    res=stream(.4,True); z=res['model']; m=6; T=32
    check('large streamed complete row renewal',res['maxrow']<2e-12,error=res['maxrow'])
    check('identical survivor WORDS give identical rows',res['maxword']<2e-14)
    check('streamed front finite-radius upper',res['maxfront']<1,ratio=res['maxfront'])
    check('streamed donor trace equality',np.ptp(res['traces'][:3])<2e-13,
          traces=res['traces'][:3].tolist())
    check('streamed corrections legal',np.min(res['gates'])>.99 and np.max(res['gates'])<1,
          last_gates=res['gates'][:3,-1].tolist())
    check('private compensator annihilators all-orders',np.linalg.norm(res['H'][:,m:m+2])<2e-12)
    check('streamed inverse-lift input cube',res['maxinput']<.5,maximum=res['maxinput'])
    check('full reference absolute input norm',res['energy']<=m*(T+2)+1,
          squared_norm=res['energy'],norm=math.sqrt(res['energy']))
    eps=1e-3
    plus=stream(.4+eps); minus=stream(.4-eps)
    fd=(plus['X']-minus['X'])/(2*eps)
    error=np.max(abs(fd-res['dX']))
    check('full derivative with exact correction vs central difference',error<3e-10,
          error=float(error),fd_step=eps)
    check('exact common endpoint across joint-prefix perturbations',np.max(abs(plus['h']-minus['h']))<1e-14)
    alt=stream(.4,change_survivor=True)
    difference=np.linalg.norm(alt['V'][3]-alt['V'][4])
    check('same last survivor gate does NOT collapse history',difference>1e-10,
          difference=float(difference),last_gates=alt['gates'][3:5,-1].tolist())
    # This pair is a microscopic formula check. One probe gives an exact
    # one-probe legal-box lower; it is not all-query distance equality.
    dx=plus['X'][:,0]-minus['X'][:,0]; odx=z.O(dx)
    hi=1/math.cosh(.25)**2; lo=1/math.cosh(.75)**2
    sigma=.05
    for _ in range(20): sigma=math.tanh(.05+sigma/(100*z.n))
    lower=sigma*math.sqrt(z.n-z.k)*z.a/(z.n*math.sqrt(z.n))*((hi+lo)/2*abs(odx.sum())+(hi-lo)/2*np.abs(odx).sum())
    check('actual one-probe legal visibility formula finite',math.isfinite(lower) and lower>0,
          numerical_lower=lower,interpretation='identity check, not robust dimension')
    del plus,minus,alt
    # Nine independent donor/epoch controls. Compensator direct derivatives
    # are zero at reset by trace equality, so these entries of dX are dH.
    columns=[]
    theta=np.full((3,3),.4)
    for i in range(3):
        for e in range(3):
            response=stream(theta,derivative=(i,e))
            dV=response['dX'][response['sites'][:,0],:m]
            dD=dV[:3].mean(axis=0)
            columns.append(np.concatenate((dV[3]-dD,dV[5]-dD)))
            del response
    transfer=np.column_stack(columns)
    spectra=np.linalg.svd(transfer,compute_uv=False)
    check('multi-epoch local transfer spectrum finite',np.all(np.isfinite(spectra)),
          spectra=spectra.tolist(),shape=list(transfer.shape),
          interpretation='infinitesimal toy diagnostic only; no finite-radius lower')

def scalar_checks():
    agreements=[]
    for bits in (192,256):
        with mp.workprec(bits):
            n=mp.mpf(10)**200; N=n/400
            ef=mp.mpf('1.275e11')*N/n**mp.mpf('1.5')
            ed=mp.mpf(816)/n**3
            full=mp.mpf('.001')+ef+ed+mp.mpf('8e-9')
            check(f'{bits} bit strict equal-code separation bound',full<mp.mpf('.002'),
                  value=mp.nstr(full,45),front=mp.nstr(ef,45),donor=mp.nstr(ed,45))
            q=mp.mpf('.9992')
            frontconst=mp.mpf('.051')*100*16000/(1-q)**2
            check(f'{bits} bit front constant',abs(frontconst-mp.mpf('1.275e11'))<mp.mpf('1e-35'))
            bottom=mp.mpf('.04')*mp.sqrt(mp.mpf(10)**6/3)-mp.log(4*mp.mpf(10)**6)
            check(f'{bits} bit exceptional public gate cap',bottom>0,value=mp.nstr(bottom,40))
            agreements.append(mp.nstr(frontconst,40))
    check('192/256 scalar constant agreement',agreements[0]==agreements[1])
    for m,T,n in ((1,200,10000),(200,1,10000),(71,71,10000),(2,4,10**6)):
        p=max(1,math.ceil(16000*math.sqrt(m*T*min(m,T))/n))
        check(f'code count cases m={m},T={T}',m*(p-1)<16000*m*T/math.sqrt(n),p=p)
    check('all loaded numerical pools limited to one',all(x.get('num_threads',1)<=1 for x in LIBRARIES),libraries=LIBRARIES)

if __name__=='__main__':
    try:
        guard(); full_small(); stream_checks(); scalar_checks(); save('PASS')
    except Exception:
        save('FAILED'); raise
