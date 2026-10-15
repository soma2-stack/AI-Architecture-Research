"""Off-cycle leak capture (PROOF.md section 5.2): two-history illustration at small n (ANALYSIS only).

A gather spike (holes on the diagonal ending at (d-1,T)) is held from row 7.
* Two off-cycle rows j, j' are held as holes (state 0, gate 1) for H steps inside the spike's
  hold, then released.
* For theta = +1 they get the balanced modulated states +-tanh(.45) for 7 steps in the middle of
  the hold; for theta = -1 they stay at 0.
* All states agree outside those 14 position-steps, so the endpoint is exact.

The script decomposes the gather row's bus difference Delta Z_T(d-1) on column j into the parts of
PROOF.md section 4.1, using the same recurrences as exp_gather_structure.py.

What it shows at n = 1024:
* the dominant part is the off-cycle leak L_own_off;
* it grows with H.

At this n its size is dominated by the off-cycle row's bath-accumulated own scalar
(~1/(1 - a ghat) ~ 285), not by the hold. The theorem-scale H^2 growth of section 5.2 sets in
only for H > ~1500 and is NOT tested here.
Run: python -I exp_offcycle_leak.py
"""
import json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def O_apply(x, k, d, gam):
    y = np.empty_like(x); y[0] = x[0]
    sp = x[1:].sum(0); J = gam * x[d - 1] / math.sqrt(k) - gam ** 2 * sp / k
    y[1] = 0.0; y[2:d] = x[1:d - 1]; y[d:] = x[d:]
    y[1:] += J; y[1] += gam * sp / math.sqrt(k)
    return y

def hist(n,H,theta,j,jp):
    k,d=n//2,n//4; l=n-k; sk=math.sqrt(k); a=1-1/n; lam=1/(100*n); gam=1/(1-1/sk)
    sig=.05
    for _ in range(100): sig=math.tanh(lam*sig+.05)
    T=2*d; Ts=T-(d-8); t0=Ts+20; t1=t0+H; tm=t0+H//2
    w=-np.ones(k)/sk; w[0]+=1; idx=np.arange(1,k)
    h=np.zeros(n); B=np.zeros((k,k)); O=np.zeros((k,k)); Y=np.zeros((k,k)); s=0.0
    tf=max(1,T-d+2)
    acc={nm:np.zeros(k) for nm in ("Kpos","Kneg","Kuni","Kbus","Lcyc","Loff","Lbus","W","Fent")}
    for t in range(1,T+1):
        hm=h[:k]; Jt=gam*hm[d-1]/sk-gam**2*hm[1:].sum()/k; beta=.05+a*Jt; s_new=math.tanh(beta+a*s)
        pre=np.empty(n); pre[:k]=a*O_apply(hm,k,d,gam)+.05; pre[k:]=lam*h[k:]+.05
        hn=np.tanh(pre); r=d-1-(T-t)
        if t>=Ts: hn[r]=0.0
        if t0<=t<t1:
            hn[j]=0.0; hn[jp]=0.0
            if tm<=t<tm+7:
                v=math.tanh(.45*(1+theta)/2); hn[j]=v; hn[jp]=-v
        s=s_new; ghat=1-s*s
        g=1-hn**2; gm=g[:k]; c=h[k:].sum()/(sig*l); delta=gm[1:]-ghat; St=delta.sum()
        Bn=a*O_apply(B,k,d,gam); Bn[idx,idx]+=c; Bn*=gm[:,None]
        Yn=Bn+(gam/sk)*(w@Bn)[None,:]; Yn[0]=Bn.sum(0)/sk
        On=np.zeros((k,k)); On[2:d]=gm[2:d,None]*a*O[1:d-1]; On[d:]=gm[d:,None]*a*O[d:]; On[idx,idx]+=c*gm[1:]
        Zp=Y-O; Zp[0]=Y[0]
        if t>=tf:
            p=d-1-(T-t)
            for nm in acc: acc[nm]*=a*gm[p]
            dp=gm[p]-ghat; Oarr=a*O[d-1]; Zarr=a*Zp[d-1]
            acc["Kpos"]+=(gam/sk)*max(dp,0)*Oarr; acc["Kneg"]+=-(gam/sk)*max(-dp,0)*Oarr
            acc["Kuni"]+=-(gam**2/k**1.5)*St*Oarr; acc["Kbus"]+=(gam/sk)*(dp-gam*St/k)*Zarr
            Osrc=np.empty((k-1,k)); Zsrc=np.empty((k-1,k))
            Osrc[0]=0; Osrc[1:d-1]=O[1:d-1]; Osrc[d-1:]=O[d:k]
            Zsrc[0]=Y[0]; Zsrc[1:d-1]=Zp[1:d-1]; Zsrc[d-1:]=Zp[d:k]
            dc_=delta.copy(); dc_[d-1:]=0; do_=delta.copy(); do_[:d-1]=0
            acc["Lcyc"]+=-(gam*a/k)*(dc_@Osrc); acc["Loff"]+=-(gam*a/k)*(do_@Osrc); acc["Lbus"]+=-(gam*a/k)*(delta@Zsrc)
            gv=gm.copy(); gv[0]=0; acc["W"]+=-(gam/k)*c*gv
            if t==tf and p==1: acc["Fent"]+=gm[1]*a*Y[0]
        h,B,Y,O=hn,Bn,Yn,On
    return acc, Y[d-1]-O[d-1]


def main():
    n = 1024; k, d = n // 2, n // 4; j, jp = d + 10, d + 11
    out = []
    for H in (25, 50, 100, 200):
        Ap, Zp = hist(n, H, 1, j, jp); Am, Zm = hist(n, H, -1, j, jp)
        parts = {nm: float((Ap[nm] - Am[nm])[j]) for nm in Ap}
        rec = {"n": n, "H": H, "dZ_on_col_j": float((Zp - Zm)[j]),
               "parts_on_col_j": parts,
               "dominant_part": max(parts, key=lambda q: abs(parts[q])),
               "reconstruction_residual": float(abs(sum(parts.values()) - (Zp - Zm)[j]))}
        print(json.dumps(rec), flush=True); out.append(rec)
    with open(os.path.join(HERE, "exp_offcycle_leak_result.json"), "w") as f:
        json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
