"""Independent constant sweep for the P1/P2 repairs (Claude, 2026-10-14).
Checks, on a log grid of n in [1e8,1e30], K in [1,n], T in [.001 sqrt n, Tcrit):
exp(kappa W) >= Q^2 when W<T; the projected (3.5) error is <= the (3.6) bound;
the totals; W sqrt(K/n)/(1+ln K); and the simplification used in Theorem 1(i).
Arithmetic only: the recurrence arguments are checked in VERIFICATION_P1_P2.md.
"""
import math
kap=1.5e-4; c=2.9e-10; Lam=4.5e5
worst={"aux":0,"eta":0,"total":0,"Wr":0,"Dsimp":0}
viol=[]
for ne in [8,9,10,12,15,20,30]:
    n=10.0**ne
    for Ke in [0,1,2,4, ne/2, ne-1, ne]:
        K=10.0**Ke
        Tcrit=c*n**1.5/(1+math.log(K))
        Tlo=0.001*math.sqrt(n)
        if Tcrit<=Tlo: continue
        for f in [i/40 for i in range(41)]:
            T=math.floor(Tlo*(Tcrit/Tlo)**f)
            if T<1 or T>=Tcrit: continue
            Q=4e4*math.sqrt(K)*max(1,(T+1)/math.sqrt(n))/kap
            Wfull=math.ceil((2/kap)*math.log(Q)); W=min(T,Wfull)
            if W<T:
                if not (kap*W>=2*math.log(Q)-1e-9): viol.append(("expQ",n,K,T))
                # auxiliary projected bound (sqrt(l)/n<=.7072/sqrt n)
                aux=.7072*math.sqrt(K)*(2*T+4*W*(T+1))*math.exp(-kap*W)/math.sqrt(n)
                delta=4e-8/n**2
                eta_exact=(math.sqrt(n/2)/n)*delta*W*math.sqrt(K)*(2*T+6*math.sqrt(n)*(T+1)/kap)  # (3.5)*proj
                eta=(7/kap)*delta*W*math.sqrt(K)*(T+1)
                if eta_exact>eta: viol.append(("36",n,K,T))
                worst["aux"]=max(worst["aux"],aux); worst["eta"]=max(worst["eta"],eta)
                worst["total"]=max(worst["total"],aux+eta)
                worst["Wr"]=max(worst["Wr"],W*math.sqrt(K/n)/(1+math.log(K)))
            # dimension-bound simplification check (i)
            L=max(0,math.log((T+1)/math.sqrt(n)))
            lhs=(2*W+Lam+1); rhs=1e6*(1+math.log(K)+L)
            worst["Dsimp"]=max(worst["Dsimp"],lhs/rhs)
print("violations:",viol[:5],len(viol))
print({k:float('%.4g'%v) for k,v in worst.items()})
