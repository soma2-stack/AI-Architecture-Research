import numpy as np, time
from harness import *
np.set_printoptions(precision=4)
for (n,F,q,seed,prot,dense) in [(200,2,3,1,0.0,"checks"),(256,3,3,2,np.sqrt(Z0/256),"checks"),(400,4,4,3,0.0,"adversarial")]:
    t0=time.time()
    M=build(n,prot,dense); d=M["d"]
    N=int(np.ceil(4*n*np.log(n)))+1
    rng=np.random.default_rng(seed)
    perp=fourier_projector(d,F)
    B=perp@rng.normal(size=(d,q))/np.sqrt(d)
    Y=rng.normal(size=(F,q)); Y/=np.linalg.norm(Y)
    S=construction_profiles(d,F,B,Y,perp)
    for delta in [0.05, 0.001]:
        cs,vs,ps=period_data(M,S,delta)
        worst={}
        for tau in range(d):
            r=step_report(M,S,delta,tau,cs,vs,ps)
            for kk,vv in r.items():
                if kk=="A_norms": continue
                worst[kk]=max(worst.get(kk,0),vv)
        Rp,maxstep=radius_periodic(M,S,delta,N,cs,vs,ps)
        Rd,lift_err,hy,h0=radius_direct(M,S,delta,N)
        print(f"n={n} F={F} delta={delta} N={N} prot={prot:.3g} dense={dense}")
        print("  decomp_err %.2e  householder_err %.2e  lift_err %.2e  endpoint |h| %.1e %.1e"%(worst['decomp_err'],worst['hh_err'],lift_err,hy,h0))
        print("  radius direct %.6e periodic %.6e rel.diff %.1e  majorant %.4e  ratio %.4f"%(Rd,Rp,abs(Rd-Rp)/Rd,majorant(n,F,delta,N),Rd/majorant(n,F,delta,N)))
        print("  worst ratios (must be <=1):", {k_:round(v_,4) for k_,v_ in worst.items() if k_ not in ('decomp_err','hh_err','dx')})
    print("  time %.1fs"%(time.time()-t0))
