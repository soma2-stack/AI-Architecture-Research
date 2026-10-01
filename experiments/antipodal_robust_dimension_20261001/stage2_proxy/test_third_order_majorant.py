import numpy as np, torch, math, itertools
torch.set_default_dtype(torch.float64); torch.set_num_threads(1)
from screen_proxy import Endpoint, SD
from explore3 import curvature3
ep=Endpoint('independent_n3_archived'); n=ep.n; r=3
B,U,s=ep.basis('query',r); a=np.array([0.2,0.3,0.4]); ah=0.01; amps=np.r_[np.full(n,ah),a]
HH,HH3,HS,HS3,rad=curvature3(ep,B,amps)
R=torch.tensor(ep.R);W=torch.tensor(ep.W);b=torch.tensor(ep.b);X0=torch.tensor(ep.X);Bt=torch.tensor(B*SD)
ER=torch.tensor(ep.ER);EW=torch.tensor(ep.EW);Eb=torch.tensor(ep.Eb);wsup=torch.tensor(ep.sw)
ii=[i for i,p in ep.support];pp=[p for i,p in ep.support]
def G(y):
    x=X0+(Bt@y).reshape(ep.T,n);h=torch.zeros(n);S=torch.zeros(n,ep.P)
    for t in range(ep.T):
        direct=torch.einsum('ipj,j->ip',ER,h)+torch.einsum('ipj,j->ip',EW,x[t])+Eb
        hn=torch.tanh(R@h+W@x[t]+b);g=1-hn*hn;S=g[:,None]*(R@S+direct);h=hn
    return torch.cat([h,S[ii,pp]*wsup])
d3=torch.func.jacfwd(torch.func.jacfwd(torch.func.jacrev(G)))
Mj=np.concatenate([HH3,HS3]);Mj2=np.concatenate([HH,HS])
rng=np.random.default_rng(0);worst=0;worst2=0
pts=[amps*np.array(c) for c in itertools.product((-1,1),repeat=n+r)][:32]+[amps*rng.uniform(-1,1,n+r) for _ in range(16)]
for y in pts:
    T3=d3(torch.tensor(y)).detach().numpy();worst=max(worst,(np.abs(T3)/np.maximum(Mj,1e-300)).max())
print('max actual|3rd derivative|/majorant over',len(pts),'points:',round(worst,5),' (<=1 required)')
