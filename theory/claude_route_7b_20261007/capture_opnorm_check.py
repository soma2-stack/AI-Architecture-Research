"""Exact check (finite R, NOT asymptotic proof) of Lemma U: the open-loop map from segment
coefficients to protected survivor content has operator norm <= 1 for one-step balanced
captures with distinct Walsh characters.  State = coefficients on Walsh characters xi_I,
I subset of {1..R} (2^R dims).  Common mode = xi_empty.  Capture e: x -> a(gbar x + b F_e x),
F_e: xi_I -> xi_{I xor e}.  Between captures: x -> a gH x (scalar, absorbed in lambda_t).
Atoms: (i) ordinary segment sigma ends just before capture sigma+1: injection = xi_empty;
(ii) capture-step injection at capture e: a(gbar xi_empty + b xi_e) then later captures.
Protected readout = projection onto nonempty characters.  Compute ||U||_op."""
import numpy as np, itertools
def opnorm(R,b,gH=1.0,a=1.0):
    dim=2**R; gbar=gH-b
    def cap(e,x):
        y=np.zeros_like(x)
        for I in range(dim):
            y[I]+=a*gbar*x[I]; y[I^(1<<e)]+=a*b*x[I]
        return y
    def after(e0,x):   # apply captures e0..R-1
        for e in range(e0,R): x=cap(e,x)
        return x
    atoms=[]
    for s in range(R+1):          # segment s: injection before capture s (s=R: after last)
        x=np.zeros(dim); x[0]=1.0; atoms.append(after(s,x))
    for e in range(R):            # capture-step injections
        x=np.zeros(dim); x[0]=a*gbar; x[1<<e]+=a*b; atoms.append(after(e+1,x))
    U=np.array(atoms).T[1:,:]     # drop common mode row (protected part only)
    Uall=np.array(atoms).T        # including common mode
    return np.linalg.norm(U,2), np.linalg.norm(Uall,2), max(np.linalg.norm(U,axis=0))
for b in [0.0025,0.05,0.2,0.4]:
    for R in [1,2,4,6,8,10]:
        u,ua,cb=opnorm(R,b)
        print(f"b={b:<7} R={R:2d}  ||U_prot||_op={u:.4f}  ||U_all||_op={ua:.4f}  max atom norm={cb:.4f}")
