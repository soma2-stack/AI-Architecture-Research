"""Reduced exact solver for the R0 autonomous fixed point (selected block via (2)-(4)),
cross-validated against brute-force iteration. Numerical check only."""
import math, numpy as np
b0=0.05
def Hof(B,a):
    lo,hi=-1+1e-15,1-1e-15
    for _ in range(200):
        mid=(lo+hi)/2
        if mid-math.tanh(a*mid+B)<0: lo=mid
        else: hi=mid
    return (lo+hi)/2
def cycle(B,n):
    k,d=n//2,n//4; a=1-1/n; tau=1/math.sqrt(k); cH=1/(1-tau)
    H=Hof(B,a); y=H
    for _ in range(6):
        v=[0.0]*(d-1); v[0]=math.tanh(a*y+B+(b0-B)/(cH*tau))
        conv=None
        for i in range(1,d-1):
            v[i]=math.tanh(a*v[i-1]+B)
            if abs(v[i]-H)<1e-17:
                conv=i; break
        if conv is not None:
            for j in range(conv+1,d-1): v[j]=H
        ynew=v[-1]
        if abs(ynew-y)<1e-17: y=ynew; break
        y=ynew
    return v,H
def solve(n):
    k,d=n//2,n//4; a=1-1/n; tau=1/math.sqrt(k); cH=1/(1-tau)
    def Phi(B):
        v,H=cycle(B,n); S=sum(v)+(k-d)*H
        return B-b0-a*cH*tau*v[-1]+a*cH*cH*tau*tau*S
    lo,hi=-0.5,b0
    assert Phi(lo)<0<Phi(hi)
    for _ in range(80):
        mid=(lo+hi)/2
        if Phi(mid)<0: lo=mid
        else: hi=mid
    B=(lo+hi)/2; v,H=cycle(B,n)
    z=Hof(b0,a); s=Hof(b0,1/(100*n))  # protected z=tanh(az+b0); source s=tanh(lambda s+b0)
    return B,v,H,z,s
def brute(n,iters_mult=40):
    k,d,l=n//2,n//4,n-n//2; a=1-1/n; tau=1/np.sqrt(k); g=1/(1-tau)
    w=-np.full(k,tau); w[0]+=1
    def O(v):
        u=v-g*w*(w@v); u=u.copy(); u[:d]=np.roll(u[:d],1); return u-g*w*(w@u)
    h=np.zeros(n)
    for _ in range(iters_mult*n):
        h=np.r_[np.tanh(a*O(h[:k])+b0),np.tanh(h[k:]/(100*n)+b0)]
    return h
for n in [2000,4000,8000]:
    B,v,H,z,s=solve(n); h=brute(n); k,d=n//2,n//4
    red=np.r_[z,np.array(v),np.full(k-d,H),np.full(n-k,s)]
    print(f"n={n}: reduced vs brute max|diff|={np.max(np.abs(red-h)):.2e}; min h*={h.min():.6f} (off-cycle H={H:.6f})")
print("n, B*, off-cycle H(B*), min cycle, protected z, source s, min coordinate")
for n in [3000,5000,10**4,3*10**4,10**5,10**6,10**7,10**8]:
    B,v,H,z,s=solve(n)
    mn=min(min(v),H,z,s)
    print(f"{n:>10d}  B*={B:.3e}  H={H:.6f}  min_cycle={min(v):.6f}  z={z:.4f}  s={s:.6f}  min={mn:.6f}  >=1/50: {mn>=0.02}")
