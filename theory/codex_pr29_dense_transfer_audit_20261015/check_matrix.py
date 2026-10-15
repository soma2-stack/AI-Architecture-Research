"""Exact rational matrix identification and Sherman-Morrison tests."""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import json

def dot(x,y): return sum(a*b for a,b in zip(x,y))
def mv(A,v): return [dot(row,v) for row in A]

def run(n):
    k=n//2; d=n//4; l=n-k; sk=isqrt(k); assert sk*sk==k
    q=F(1,sk); ga=1/(1-q); a=1-F(1,n); lam=F(1,100*n)
    w=[-q]*k; w[0]+=1
    U=[[F(i==j)-ga*w[i]*w[j] for j in range(k)] for i in range(k)]
    # P U, by rows; P cycles 0,...,d-1 forward.
    PU=[row.copy() for row in U]; PU[0]=U[d-1]; PU[1:d]=U[:d-1]
    O=[[dot(row,col) for col in zip(*PU)] for row in U]
    O1=mv(O,[F(1)]*k); OT1=mv(list(zip(*O)),[F(1)]*k)
    predicted=[-ga*q]*k; predicted[0]=1; predicted[d-1]=(k-ga)*q
    assert OT1==predicted
    predicted=[-ga*q]*k; predicted[0]=1; predicted[1]=(k-ga)*q
    assert O1==predicted
    assert all(O1) and all(OT1)
    R0=[[F(0)]*n for _ in range(n)]; inv0=[[F(0)]*n for _ in range(n)]
    for i in range(k):
        for j in range(k): R0[i][j]=a*O[i][j]; inv0[i][j]=O[j][i]/a
    for i in range(k,n): R0[i][i]=lam; inv0[i][i]=1/lam
    left=mv(inv0,[F(1)]*n); right=mv(list(zip(*inv0)),[F(1)]*n)
    assert all(left) and all(right)
    assert sum(left)==F(l)/lam
    eta=F(1,10**8*n*n)
    B=[[v+eta/n for v in row] for row in R0]
    denominator=1+eta/n*sum(left)
    inverse=[[inv0[i][j]-eta/n*left[i]*right[j]/denominator for j in range(n)] for i in range(n)]
    assert all(v for row in B for v in row)
    assert all(v for row in inverse for v in row)
    for v in ([F(1)]*n,[F(i%7-3) for i in range(n)]): assert mv(inverse,mv(B,v))==v
    return dict(n=n,t_left=1,t_right=1,first_eta_index=0,
                min_inverse_image=str(min(map(abs,left))),
                exact_B_inverse_checks=True,gamma=str(ga))

if __name__=='__main__':
    results=[run(n) for n in (8,9,18,32,50,72)]
    (Path(__file__).resolve().parent/'matrix_results.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(results,indent=2))
