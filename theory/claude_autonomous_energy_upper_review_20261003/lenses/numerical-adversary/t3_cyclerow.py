import numpy as np, math
from model import Model
from sim import Sim
n=8000; M=Model(n); hs=M.polish(M.fixed_point(),20); k,d=M.k,M.d; ath=np.arctanh(hs)
B0=6000; Th=d-3; jend=d-2
def pol(t,h,pre):
    if t<=B0: return None
    if t<=B0+Th:
        j=jend-(B0+Th-t); return (np.array([j]),np.array([-pre[j]]))
    if t==B0+Th+1: return ath-pre
    return None
T=B0+Th+1
S=Sim(M,hs,pol,T,ckpt=500)
y=np.zeros(n); y[d-1]=1.0
w=S.adjoint(y)[0]          # indexes selected coords 1..k-1 -> w[j-1]
path=np.arange(jend-Th+1,jend+1)
print("energy",S.energy,"sigma",hs[k])
print("||M^* e_{d-1}||=",np.linalg.norm(w)," on path:",np.linalg.norm(w[path-1])," off path:",np.linalg.norm(np.delete(w,path-1)))
print("predicted sigma*sqrt(sum A^{2(T-s)}):",hs[k]*math.sqrt(sum(M.A**(2*(Th-i)) for i in range(Th))))
print("path entries (first,mid,last):",w[path[0]-1],w[path[len(path)//2]-1],w[path[-1]-1])
# compare: no-burn-in version from t=1 (as in exp_main)
wp=w[path-1]
idx=np.linspace(0,len(path)-1,12).astype(int)
print("profile along path (pos, w, sigma*A^(T-s)):")
for q in idx:
    j=path[q]; s=T-1-(jend-j)   # time when hole at j
    print(j, round(wp[q],5), round(hs[k]*M.A**(T-s),5), "h*_j=",round(hs[j],4))
# check gates along hole at a few times by re-simulating
h=np.zeros(n)
for t in range(1,T+1):
    pre=M.R(h)+0.05; x=pol(t,h,pre)
    if x is None: h=np.tanh(pre)
    elif isinstance(x,tuple): pre[x[0]]+=x[1]; h=np.tanh(pre)
    else: h=np.tanh(pre+x)
    if t in (B0+1,B0+10,B0+Th//2,B0+Th):
        j=jend-(B0+Th-t); print("t",t,"hole j",j,"h_j",h[j],"h_{j+1}",h[j+1],"h_{j-1}",h[j-1])
