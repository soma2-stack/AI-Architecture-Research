import numpy as np, mpmath as mp
from harness import build
mp.mp.dps=40
b0=mp.mpf(1)/20; A=mp.atanh(mp.mpf(2)/5)
C=mp.sqrt(2*(b0**2+(A-b0)**2)); print("C_abs =",mp.nstr(C,30))
def E0(n):
    nn=mp.mpf(n); k,l=n//2,n-n//2; a=1-1/nn; lam=1/(100*nn); s=mp.mpf(2)/5; beta=mp.sqrt(mp.mpf(3)/(20*nn)); B=mp.atanh(beta)
    N=int(mp.ceil(4*nn*mp.log(nn)))+1
    return mp.sqrt(k*(2*b0**2+N*((B-b0)**2+a**2*beta**2))+l*((A-b0)**2+N*(A-b0-lam*s)**2+(b0+lam*s)**2)),N
for n in [200,256,400,1000,2000,10**6,10**9,10**15,10**30]:
    e,N=E0(n); print(f"n={n}: E0={mp.nstr(e,13)}  E0/(n sqrt log n)={mp.nstr(e/(n*mp.sqrt(mp.log(n))),12)}  rel.gap to C_abs={mp.nstr(1-e/(n*mp.sqrt(mp.log(n)))/C,4)}")
# actual dense R center via exact formula (1)
for n in [200,256,400]:
    M=build(n,protected_value=np.sqrt(0.15/n)); R=M["R"]; k,l=M["k"],M["ell"]
    p=np.r_[np.zeros(k),np.full(l,.4)]; v=np.r_[np.full(k,np.sqrt(.15/n)),np.full(l,.4)]; q=np.arctanh(v)-.05
    N=int(np.ceil(4*n*np.log(n)))+1
    ER=np.sqrt(np.sum((np.arctanh(p)-.05)**2)+np.sum((q-R@p)**2)+(N-1)*np.sum((q-R@v)**2)+np.sum((R@v+.05)**2))
    e0=float(E0(n)[0]); dn=4/(1e8*n**2)*np.sqrt(.16*l+N*(.15/n*k+.16*l))
    print(f"n={n}: actual-R center {ER:.9f}  E0 {e0:.9f}  |diff| {abs(ER-e0):.2e}  Delta_n {dn:.2e}  inside: {abs(ER-e0)<=dn}")
# autonomous fixed point h* of F(h)=tanh(Rh+b0)
for n in [200,400,800]:
    M=build(n); R=M["R"]; k,l=M["k"],M["ell"]
    h=np.zeros(n)
    for it in range(60*n):
        h=np.tanh(R@h+0.05)
    resid=np.linalg.norm(h-np.tanh(R@h+0.05))
    hm,hs=h[:k],h[k:]
    print(f"n={n}: ||F(h*)-h*||={resid:.1e} | source h*: {hs.min():.6f}..{hs.max():.6f} (tanh(b0)={np.tanh(.05):.6f}) | memory |h*| max {np.abs(hm).max():.4f}, #|h|>0.9: {int(np.sum(np.abs(hm)>.9))}, #|h|<1/(2sqrt n): {int(np.sum(np.abs(hm)<=1/(2*np.sqrt(n))))}/{k}, min gate {np.min(1-hm**2):.4f}"
          f" | source terminal bound (15) at z=h*: {np.linalg.norm(np.arctanh(hs)-.05)-np.sqrt(l)/(100*n)-4/(1e8*n**1.5):.3e}")
