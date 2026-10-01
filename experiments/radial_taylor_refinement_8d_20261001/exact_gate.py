"""Rigorous polynomial-extremum gate majorants; no midpoint certificates."""
from fractions import Fraction as Q
import numpy as np
from antipodal_kernel import I,uq
POLYS=((1,0,-1),(0,-2,0,2),(-2,0,8,0,-6),(0,16,0,-40,0,24))
CACHE={}
def evaluate(coeff,x):
    y=I(0)
    for v in reversed(coeff):y=y*x+v
    return y
def roots():
    if I.bits not in CACHE:
        a=I(Q(1,3)).sqrt();b=I(Q(2,3)).sqrt();q=I(105).sqrt()
        lo=((15-q)/30).sqrt();hi=((15+q)/30).sqrt()
        CACHE[I.bits]=((I(0),),(a,-a),(I(0),b,-b),(lo,-lo,hi,-hi))
    return CACHE[I.bits]
def polynomial_upper(j,x):
    points=[I(x.lo,x.lo,True),I(x.hi,x.hi,True)]
    points.extend(v for v in roots()[j] if v.hi>=x.lo and v.lo<=x.hi)
    return max(evaluate(POLYS[j],p).absq() for p in points)
def gate_majorants(h):
    out=[[] for _ in range(4)]
    for x in h:
        g=I(1)-x.square()
        old=(Q(g.hi,I.scale),(2*x*g).absq(),(-2*g*(I(1)-3*x.square())).absq(),
             (8*x*g*(I(2)-3*x.square())).absq())
        for j in range(4):out[j].append(uq(min(old[j],polynomial_upper(j,x))))
    return tuple(np.array(row) for row in out)
