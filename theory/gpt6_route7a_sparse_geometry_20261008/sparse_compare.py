"""Cross-validate sparse chronological public history and adjoint against
the independently archived corrected dense reference history.
This test requires NumPy and the adjacent theory folder.
"""
import math,json,time,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/
                      "gpt6_route7a_chronological_public_20261007"))
from chronological_probe import make_history,Mt
from sparse_geometry import sparse_history,sparse_Mt,apply_OT

def check(n,m,R):
    tic=time.time()
    pos=np.ones((R,m))
    sp=sparse_history(n,m,R,pos)
    dn=make_history(n,m,R,pos)
    mx=0.
    for old,(bulk,idx,diff) in zip(dn['gates'],sp['gates']):
        rebuilt=np.full_like(old,bulk)
        rebuilt[idx]+=diff
        mx=max(mx,float(np.max(abs(rebuilt-old))))
    full=np.full_like(dn['endpoint'],sp['base'])
    for i,delta in sp['exceptions'].items():full[i]+=delta
    end=float(np.max(abs(full-dn['endpoint'])))
    ghi=1/math.cosh(.25)**2
    c=(1-1/n)*apply_OT(n,np.full(n//2-1,ghi))/math.sqrt(n)
    z1=Mt(n,dn['gates'],c)
    z2=sparse_Mt(n,sp['gates'],c)
    relative=float(np.linalg.norm(z1-z2)/max(1.,np.linalg.norm(z1)))
    assert mx<1e-12 and end<1e-12 and relative<1e-12
    return dict(n=n,m=m,R=R,max_gate_error=mx,
       hidden_endpoint_error=end,adjoint_relative_error=relative,
       max_exception_rows=sp['maxexception'],elapsed_s=round(time.time()-tic,2))

if __name__=='__main__':
    for n,m,R in [(16384,4,2),(32768,8,4),(65536,32,16)]:
        print(json.dumps(check(n,m,R)),flush=True)
