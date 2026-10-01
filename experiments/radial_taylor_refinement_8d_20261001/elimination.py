"""Exact final-input sensitivity identity and rigorous prefix contractions."""
from fractions import Fraction as Q
import numpy as np
import common as c
k=c.ref;I=k.I
def matrices(base):
    m=base['model'];n=m.n;R=[[Q(0) for _ in range(n)] for _ in range(n)];W=[[Q(0) for _ in range(n)] for _ in range(n)];b=[Q(0)]*n
    for i,j,p in m.layers[0]['R']:R[i][j]=m.params[p]
    for i,j,p in m.layers[0]['W']:W[i][j]=m.params[p]
    for i,j,p in m.layers[0]['b']:b[i]=m.params[p]
    assert m.diagonal and m.n==4 and m.P==24
    return R,W,b
def coefficients(base,ell):
    R,W,b=matrices(base);Wi=k.inverse(W);h=[I(0) for _ in b]
    for x in base['X']:
        h=[(sum((I(R[i][j])*h[j]+I(W[i][j])*I(x[j]) for j in range(4)),I(b[i]))).tanh() for i in range(4)]
    g=[I(1)-v.square() for v in h];m=base['model'];r=len(ell)
    CS=[[I(0) for _ in m.support] for _ in range(r)];CH=[[I(0) for _ in range(4)] for _ in range(r)]
    for a in range(r):
        for q,(owner,p) in enumerate(m.support):
            _,i,name,j=m.meta[p];v=I(ell[a][q])*g[owner];sw=base['scaleI'][name]
            CS[a][q]=v*R[owner][owner]
            if name=='R':CH[a][j]+=v*sw
            elif name=='W':
                for z in range(4):CH[a][z]-=v*sw*Wi[j][z]*R[z][z]
    return CS,CH,{'gate_intervals':[[str(Q(v.lo,I.scale)),str(Q(v.hi,I.scale))] for v in g]}
def prefix_bound(base,aa,lam,CS,CH,kernel):
    n=base['n'];r=len(aa);prefix=dict(base)
    prefix['X']=base['X'][:-1];prefix['BI']=base['BI'][:-n];prefix['B']=base['B'][:-n]
    assert all(v.lo==0 and v.hi==0 for row in prefix['BI'] for v in row[:n])
    HH,HH3,HS,HS3=kernel.third_majorants(prefix,r,[Q(0)]*n+[lam*a for a in aa])
    # Every mixed tangent derivative remains. Coefficients include 1/a_i.
    PHI3=k.upadd(k.left(k.abs_array(CS),HS3[:,n:,n:,n:]),k.left(k.abs_array(CH),HH3[:,n:,n:,n:]))
    a=np.array([k.uq(v) for v in aa])
    M=k.upsum(k.upsum(k.upsum(kernel.times(PHI3,a[None,:,None,None],a[None,None,:,None],a[None,None,None,:]),axis=3),axis=2),axis=1)
    return [Q(float(v)) for v in M],{'HH':HH,'HH3':HH3,'HS':HS,'HS3':HS3,'Phi3':PHI3}
