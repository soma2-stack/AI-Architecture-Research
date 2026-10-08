"""Finite checks for the isolated local-C three-step moving characteristic.
The proof in PROOF.md is analytic. These checks are illustrative only.
Run: python local_row_checks.py
"""
import math
import random

G=.9975
E=.0001
GH=.99999
A=1-1/1000000
LSTAR=(G/(G-E))**2
RHO=(G+E)*G*G/(G-E)
assert LSTAR*(2/(.99**3)*1.25+math.sqrt(2))<4
assert RHO<1
rowbound=8*E/(1-RHO)
assert rowbound<.16687
assert .051*rowbound<.00852

def one_history(c,R,L,wait):
    row=[]
    tau=0.
    def update(d):
        nonlocal tau
        row[:]=[a*A*d for a in row]+[d]
        tau=d*(1+A*tau)
    for _ in range(L):update(GH)
    for j in range(R):
        for _ in range(wait):update(GH)
        incoming=tau
        d1=G+E*c[j]
        trgt=G*(1+A*GH*(1+A*G*(1+A*incoming)))
        mid=GH*(1+A*d1*(1+A*incoming))
        d3=trgt/(1+A*mid)
        update(d1)
        update(GH)
        update(d3)
        assert abs(tau-trgt)<1e-8
    return row,tau

random.seed(17837)
for R in (1,8,32,128,512):
    x=[random.uniform(-1,1) for _ in range(R)]
    for wait in (0,4):
        rx,tx=one_history(x,R,500,wait)
        ry,ty=one_history([-v for v in x],R,500,wait)
        norm=math.sqrt(sum((v-w)**2 for v,w in zip(rx,ry)))
        assert abs(tx-ty)<1e-8
        assert norm<rowbound
        print("R=%d wait=%d trace_gap=%.2g moving_row_norm=%.9f bound=%.6f" %
              (R,wait,tx-ty,norm,rowbound))
