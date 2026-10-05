"""Forward-simulate the public center history with the ACTUAL archived dense R (not R0, not a test
perturbation), check endpoint h=0, exact ||X||, eq.(1), and sandwich (5) with E0 from eq.(3)."""
import os; os.environ["OMP_NUM_THREADS"]="2"
import sys, json, numpy as np, mpmath as mp
sys.path.insert(0, "/home/user/AI-Architecture-Research/theory/claude_bounded_history_radius_review_20261003")
from harness import build
b0=0.05; s=0.4
out=[]
for n in (200, 256, 400):
    M=build(n, dense="checks"); R=M["R"]; k,l=M["k"],M["ell"]
    beta=np.sqrt(0.15/n); N=int(np.ceil(4*n*np.log(n)))+1
    p=np.r_[np.zeros(k), np.full(l,s)]; v=np.r_[np.full(k,beta), np.full(l,s)]
    states=[p]+[v]*N+[np.zeros(n)]
    h=np.zeros(n); sq=0.0; maxin=0.0; endpoint_err=0.0; maxstate_err=0.0
    for tgt in states:
        x=np.arctanh(tgt)-R@h-b0
        maxin=max(maxin, np.abs(x).max())
        hn=np.tanh(R@h+x+b0)
        maxstate_err=max(maxstate_err, np.abs(hn-tgt).max())
        sq+=x@x; h=hn
    q=np.arctanh(v)-b0
    eq1=np.sqrt(np.linalg.norm(np.arctanh(p)-b0)**2+np.linalg.norm(q-R@p)**2+(N-1)*np.linalg.norm(q-R@v)**2+np.linalg.norm(R@v+b0)**2)
    with mp.workdps(50):
        nn=mp.mpf(n); a=1-1/nn; lam=1/(100*nn); B=mp.atanh(mp.sqrt(mp.mpf(3)/(20*nn))); A=mp.atanh(mp.mpf(2)/5); bb=mp.mpf(1)/20; be=mp.sqrt(mp.mpf(3)/(20*nn)); ss=mp.mpf(2)/5
        E0=mp.sqrt(k*(2*bb**2+N*((B-bb)**2+a*a*be*be))+l*((A-bb)**2+N*(A-bb-lam*ss)**2+(bb+lam*ss)**2))
        Dn=4/(10**8*nn**2)*mp.sqrt(ss*ss*l+N*(be*be*k+ss*ss*l))
    row=dict(n=n,N=N,steps=len(states),X_norm_forward=float(np.sqrt(sq)),eq1=float(eq1),E0=float(E0),Delta_n=float(Dn),
             forward_minus_E0=float(np.sqrt(sq)-E0), within_sandwich=bool(abs(np.sqrt(sq)-float(E0))<=float(Dn)+1e-9),
             endpoint_maxabs=float(np.abs(h).max()), max_state_err=float(maxstate_err), max_abs_input=float(maxin),
             final_reset_norm=float(np.linalg.norm(-R@v-b0)), L_n=float((b0-1/(100*n))*np.sqrt(l)-4e-8/n**1.5))
    out.append(row); print(json.dumps(row))
json.dump(out, open("center_forward.json","w"), indent=1)
